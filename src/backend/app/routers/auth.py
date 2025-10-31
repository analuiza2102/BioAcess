"""Rotas de autenticação: enroll e verify"""

from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
import base64
import io
from PIL import Image
from ..db import get_db
from ..models import User, BiometricTemplate
from ..services.biometric_engine import extract_embedding, verify_match, cosine_similarity
from ..config import settings
from ..services.liveness import validate_liveness
from ..services.audit import log_action
from ..security import create_access_token, verify_password
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["autenticação"])

# Configuração do bcrypt para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    """Request para criar novo usuário"""
    username: str
    password: str
    role: str = "public"  # padrão: public
    clearance: int = 1    # padrão: nível 1

class EnrollRequest(BaseModel):
    """Request para cadastro de biometria via upload de imagem"""
    username: str
    image_b64: str
    image_format: str = "jpeg,png,jpg"  # jpeg, png, jpg, etc



class VerifyRequest(BaseModel):
    """Request para verificação biométrica via upload de imagem"""
    username: str
    image_b64: str
    image_format: str = "jpeg,png,jpg"  # jpeg, png, jpg, etc


class LoginRequest(BaseModel):
    """Request para login tradicional com senha"""
    username: str
    password: str


class CheckBiometricRequest(BaseModel):
    """Request para verificar se usuário tem biometria cadastrada"""
    username: str


@router.post("/create-user")
async def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db)
):
    """
    Cria um novo usuário no sistema para testes.
    
    Permite criação livre de usuários para demonstração.
    """
    # Verificar se usuário já existe
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Usuário já existe")
    
    # Validar role
    valid_roles = ["public", "director", "minister"]
    if data.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Role deve ser: {valid_roles}")
        
    # Validar clearance
    if data.clearance not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Clearance deve ser 1, 2 ou 3")
        
    try:
        # Criar hash da senha
        hashed_password = pwd_context.hash(data.password)
        
        # Criar usuário
        new_user = User(
            username=data.username,
            password_hash=hashed_password,
            role=data.role,
            clearance=data.clearance
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "success": True,
            "message": "Usuário criado com sucesso!",
            "user_id": new_user.id,
            "username": new_user.username,
            "role": new_user.role,
            "clearance": new_user.clearance
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")


@router.post("/enroll")
async def enroll_biometric(
    request: Request,
    data: EnrollRequest,
    db: Session = Depends(get_db)
):
    """
    Cadastra biometria facial de um usuário.
    
    O usuário deve existir previamente no banco de dados.
    Não permite recadastro (biometria já cadastrada).
    
    Returns:
        - success: bool
        - message: str
        - user_id: int
    """
    # Verifica se usuário existe
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado no sistema")
    
    # Verifica se já tem biometria cadastrada
    existing = db.query(BiometricTemplate).filter(
        BiometricTemplate.user_id == user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail="Usuário já possui biometria cadastrada")
    
    try:
        # Extrai embedding facial
        embedding = extract_embedding(data.image_b64)
        
        # Salva template biométrico
        template = BiometricTemplate(
            user_id=user.id,
            embedding=embedding
        )
        db.add(template)
        db.commit()
        
        # Registra no log de auditoria
        log_action(
            db, data.username, "enroll", True,
            origin_ip=request.client.host if request.client else None
        )
        
        return {
            "success": True,
            "message": "Biometria cadastrada com sucesso",
            "user_id": user.id
        }
        
    except ValueError as e:
        log_action(db, data.username, "enroll", False)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log_action(db, data.username, "enroll", False)
        raise HTTPException(status_code=500, detail="Erro ao processar biometria")


@router.post("/verify")
async def verify_biometric(
    request: Request,
    data: VerifyRequest,
    db: Session = Depends(get_db)
):
    """
    Verifica biometria facial via upload de imagem.
    
    O usuário envia uma imagem (PNG/JPEG) que será comparada
    com o template biométrico previamente cadastrado.
    
    Recomenda-se usar imagens com fundo branco para melhor precisão.
    
    Returns:
        - token: JWT para autenticação
        - role: Papel do usuário (public, director, minister)
        - clearance: Nível de acesso (1, 2, 3)
        - username: Nome do usuário
    """
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user:
        log_action(db, data.username, "verify", False)
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    template = db.query(BiometricTemplate).filter(
        BiometricTemplate.user_id == user.id
    ).first()
    
    if not template:
        log_action(db, data.username, "verify", False)
        raise HTTPException(status_code=404, detail="Biometria não cadastrada para este usuário")
    
    try:
        print(f"🔍 Verificação biométrica para usuário: {data.username}")
        print(f"📸 Formato da imagem: {data.image_format}")
        
        # Extrai embedding da imagem enviada
        test_embedding = extract_embedding(data.image_b64)
        
        # Verifica match com template cadastrado
        if not verify_match(template.embedding, test_embedding):
            log_action(db, data.username, "verify", False)
            raise HTTPException(status_code=401, detail="Imagem não corresponde ao usuário cadastrado")
        
        # Sucesso - gera JWT
        token = create_access_token({"sub": user.username})
        
        log_action(
            db, data.username, "verify", True,
            origin_ip=request.client.host if request.client else None
        )
        
        print(f"✅ Verificação bem-sucedida para {data.username}")
        
        return {
            "token": token,
            "role": user.role,
            "clearance": user.clearance,
            "username": user.username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log_action(db, data.username, "verify", False)
        print(f"❌ Erro na verificação: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar verificação biométrica")


@router.post("/login")
async def traditional_login(
    request: Request,
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login tradicional com usuário e senha.
    
    Returns:
        - access_token: JWT para autenticação
        - role: Papel do usuário (public, director, minister)
        - clearance_level: Nível de acesso (1, 2, 3)
        - username: Nome do usuário
    """
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user:
        log_action(db, data.username, "login", False)
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Verifica senha
    if not verify_password(data.password, user.password_hash):
        log_action(
            db, data.username, "login", False,
            origin_ip=request.client.host if request.client else None
        )
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Gera JWT
    token = create_access_token({"sub": user.username})
    
    log_action(
        db, data.username, "login", True,
        origin_ip=request.client.host if request.client else None
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "clearance": user.clearance,
        "username": user.username
    }


@router.post("/check-biometric")
async def check_biometric_exists(
    data: CheckBiometricRequest,
    db: Session = Depends(get_db)
):
    """
    Verifica se um usuário possui biometria cadastrada.
    
    Returns:
        - has_biometric: bool
        - message: str
    """
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    template = db.query(BiometricTemplate).filter(
        BiometricTemplate.user_id == user.id
    ).first()
    
    has_biometric = template is not None
    
    return {
        "has_biometric": has_biometric,
        "message": "Biometria encontrada" if has_biometric else "Biometria não cadastrada"
    }


@router.post("/enroll-upload")
async def enroll_biometric_upload(
    request: Request,
    username: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Cadastra biometria facial via upload de arquivo de imagem.
    
    Formatos suportados: PNG, JPEG, JPG
    Recomenda-se usar imagens com fundo branco para melhor precisão.
    
    Args:
        username: Nome do usuário
        image: Arquivo de imagem (PNG, JPEG, JPG)
        
    Returns:
        - success: bool
        - message: str
        - user_id: int
    """
    # Validar formato do arquivo
    allowed_formats = ["image/jpeg", "image/jpg", "image/png"]
    if image.content_type not in allowed_formats:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de imagem não suportado. Use: PNG, JPEG ou JPG"
        )
    
    # Verifica se usuário existe
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado no sistema")
    
    # Verifica se já tem biometria cadastrada
    existing = db.query(BiometricTemplate).filter(
        BiometricTemplate.user_id == user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail="Usuário já possui biometria cadastrada")
    
    try:
        # Lê o arquivo de imagem
        image_data = await image.read()
        
        # Converte para base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        print(f"📸 Processando cadastro biométrico para {username}")
        print(f"📁 Formato: {image.content_type}, Tamanho: {len(image_data)} bytes")
        
        # Extrai embedding facial
        embedding = extract_embedding(image_b64)
        
        # Salva template biométrico
        template = BiometricTemplate(
            user_id=user.id,
            embedding=embedding
        )
        db.add(template)
        db.commit()
        
        # Registra no log de auditoria
        log_action(
            db, username, "enroll", True,
            origin_ip=request.client.host if request.client else None
        )
        
        print(f"✅ Biometria cadastrada com sucesso para {username}")
        
        return {
            "success": True,
            "message": "Biometria cadastrada com sucesso via upload de imagem",
            "user_id": user.id
        }
        
    except ValueError as e:
        log_action(db, username, "enroll", False)
        print(f"❌ Erro na extração de features: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erro ao processar imagem: {str(e)}")
    except Exception as e:
        log_action(db, username, "enroll", False)
        print(f"❌ Erro interno: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar biometria")


@router.post("/verify-upload")
async def verify_biometric_upload(
    request: Request,
    username: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Verifica biometria facial via upload de arquivo de imagem.
    
    Formatos suportados: PNG, JPEG, JPG
    Recomenda-se usar imagens com fundo branco para melhor precisão.
    
    Args:
        username: Nome do usuário
        image: Arquivo de imagem (PNG, JPEG, JPG)
        
    Returns:
        - token: JWT para autenticação
        - role: Papel do usuário
        - clearance: Nível de acesso
        - username: Nome do usuário
    """
    # Validar formato do arquivo
    allowed_formats = ["image/jpeg", "image/jpg", "image/png"]
    if image.content_type not in allowed_formats:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de imagem não suportado. Use: PNG, JPEG ou JPG"
        )
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        log_action(db, username, "verify", False)
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    template = db.query(BiometricTemplate).filter(
        BiometricTemplate.user_id == user.id
    ).first()
    
    if not template:
        log_action(db, username, "verify", False)
        raise HTTPException(status_code=404, detail="Biometria não cadastrada para este usuário")
    
    try:
        # Lê o arquivo de imagem
        image_data = await image.read()
        
        # Converte para base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        print(f"🔍 Verificação biométrica para usuário: {username}")
        print(f"📁 Formato: {image.content_type}, Tamanho: {len(image_data)} bytes")
        
        # Extrai embedding da imagem enviada
        test_embedding = extract_embedding(image_b64)
        
        # Verifica match com template cadastrado
        if not verify_match(template.embedding, test_embedding):
            log_action(db, username, "verify", False)
            raise HTTPException(status_code=401, detail="Imagem não corresponde ao usuário cadastrado")
        
        # Sucesso - gera JWT
        token = create_access_token({"sub": user.username})
        
        log_action(
            db, username, "verify", True,
            origin_ip=request.client.host if request.client else None
        )
        
        print(f"✅ Verificação bem-sucedida para {username}")
        
        return {
            "token": token,
            "role": user.role,
            "clearance": user.clearance,
            "username": user.username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log_action(db, username, "verify", False)
        print(f"❌ Erro na verificação: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar verificação biométrica")


@router.post("/verify-camera")
async def verify_biometric_camera(
    request: Request,
    username: str = Form(...),
    camera_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Verifica login biométrico usando câmera.
    
    Compara a imagem capturada da câmera com a biometria cadastrada.
    Esta é a funcionalidade principal para login por reconhecimento facial.
    
    Args:
        username: Nome do usuário
        camera_image: Imagem capturada da câmera (PNG/JPEG)
        
    Returns:
        - token: JWT para autenticação
        - role: Papel do usuário 
        - clearance: Nível de acesso
        - username: Nome do usuário
    """
    # Validar tipo de arquivo
    if camera_image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use PNG ou JPEG.")
    
    # Verificar se usuário existe
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        log_action(db, username, "camera_verify", False, 
                  origin_ip=request.client.host if request.client else None)
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar se possui biometria cadastrada
    template = db.query(BiometricTemplate).filter(
        BiometricTemplate.user_id == user.id
    ).first()
    
    if not template:
        log_action(db, username, "camera_verify", False,
                  origin_ip=request.client.host if request.client else None)
        raise HTTPException(status_code=404, detail="Biometria não cadastrada para este usuário")

    try:
        # Ler imagem da câmera
        camera_data = await camera_image.read()
        camera_b64 = base64.b64encode(camera_data).decode()
        
        print(f"📷 Processando login por câmera para usuário: {username}")
        print(f"📁 Tamanho da imagem: {len(camera_data)} bytes")
        print(f"📄 Content-Type: {camera_image.content_type}")
        
        # Extrair embedding da imagem capturada
        print("🧠 Iniciando extração de embedding da câmera...")
        camera_embedding = extract_embedding(camera_b64)
        print(f"✅ Embedding da câmera extraído: {len(camera_embedding)} dimensões")
        
        # Comparar com embedding cadastrado
        stored_embedding = template.embedding
        print(f"📊 Template armazenado: {len(stored_embedding)} dimensões")
        
        similarity = cosine_similarity(camera_embedding, stored_embedding)
        
        print(f"📊 Similaridade: {similarity:.4f}")
        print(f"📏 Threshold: {settings.SIMILARITY_THRESHOLD}")
        
        # Verificar se a similaridade está acima do threshold
        if similarity >= settings.SIMILARITY_THRESHOLD:
            # Login bem-sucedido
            token_data = {"sub": user.username, "role": user.role}
            access_token = create_access_token(data=token_data)
            
            log_action(db, username, "camera_verify", True,
                      origin_ip=request.client.host if request.client else None)
            
            return {
                "access_token": access_token,
                "token_type": "bearer", 
                "role": user.role,
                "clearance": user.clearance,
                "username": user.username,
                "message": "Login por reconhecimento facial realizado com sucesso"
            }
        else:
            # Falha na verificação
            log_action(db, username, "camera_verify", False,
                      origin_ip=request.client.host if request.client else None)
            raise HTTPException(status_code=401, detail="Reconhecimento facial falhou. Rosto não reconhecido.")
            
    except HTTPException:
        raise
    except Exception as e:
        log_action(db, username, "camera_verify", False,
                  origin_ip=request.client.host if request.client else None)
        print(f"❌ Erro no login por câmera: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao processar reconhecimento facial")
