from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os
import jwt
from datetime import datetime, timedelta
import io
from PIL import Image
import numpy as np
import face_recognition

from app.config import get_db, Base, engine
from app.models.user import User
from app.models.biometric_template import BiometricTemplate

router = APIRouter(prefix="/auth", tags=["auth"])

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# Create a demo user if DB is empty (only for first run / local tests)
from sqlalchemy import select
def _ensure_demo_user(db: Session):
    try:
        exists = db.execute(select(User).where(User.username == "ana.luiza")).scalar_one_or_none()
        if not exists:
            pwd_hash = pwd_context.hash("senha123")
            db.add(User(username="ana.luiza", password_hash=pwd_hash, role="public", clearance=1))
            db.commit()
            print("✅ Usuário demo 'ana.luiza' criado")
    except Exception as e:
        print(f"⚠️ Erro ao criar usuário demo: {e}")
        db.rollback()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Dependency para obter usuário atual do token JWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Extrai e valida o token JWT, retornando os dados do usuário.
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        return {"username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais"
        )

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login_user(body: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user with JSON payload {username, password}. Returns JWT.
    This endpoint is JSON-based to match the current frontend implementation.
    """
    try:
        print(f"🔐 Tentativa de login: username={body.username}")

        from sqlalchemy import select
        user = db.execute(select(User).where(User.username == body.username)).scalar_one_or_none()
        if not user:
            print(f"❌ Usuário não encontrado: {body.username}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        print(f"✅ Usuário encontrado: {user.username}, verificando senha...")
        if not pwd_context.verify(body.password, user.password_hash):
            print(f"❌ Senha incorreta para: {body.username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta")

        print(f"✅ Senha correta, gerando token...")
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

        print(f"✅ Login bem-sucedido: {user.username}")
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user.username,
            "role": user.role,
            "clearance": user.clearance
        }
    except HTTPException:
        raise
    except Exception as e:
        # Log server-side and return a clean message
        print("❌ Erro interno no /auth/login:", repr(e))
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.post("/login/camera")
async def login_by_camera(
    username: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Login via reconhecimento facial usando câmera
    Usa face_recognition (dlib) para detecção e verificação facial
    """
    try:
        # Verificar se usuário existe
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        print(f"🔍 Processando reconhecimento facial para usuário: {username}")
        
        # Ler imagem e converter para RGB
        image_bytes = await image.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        # Converter para RGB se necessário
        if img.mode != 'RGB':
            img = img.convert('RGB')
            print(f"🔄 Imagem convertida para RGB")
        
        img_array = np.array(img)
        print(f"📐 Shape da imagem: {img_array.shape}")
        
        # Verificar se usuário tem biometria cadastrada
        biometric = db.execute(
            select(BiometricTemplate).where(BiometricTemplate.user_id == user.id)
        ).scalar_one_or_none()
        
        if not biometric:
            print(f"❌ Usuário {username} não possui biometria cadastrada")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não possui biometria cadastrada. Cadastre sua biometria primeiro."
            )
        
        print(f"✅ Biometria encontrada para user_id={user.id}")
        
        # Usar face_recognition para detecção e comparação
        try:
            # Detectar faces na imagem
            face_locations = face_recognition.face_locations(img_array)
            
            if not face_locations or len(face_locations) == 0:
                print(f"❌ Nenhuma face detectada na imagem")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Nenhuma face detectada na imagem. Use uma foto clara com seu rosto visível."
                )
            
            print(f"✅ {len(face_locations)} face(s) detectada(s)")
            
            # Gerar encoding da face capturada
            current_encodings = face_recognition.face_encodings(img_array, face_locations)
            
            if not current_encodings or len(current_encodings) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Não foi possível processar a face detectada"
                )
            
            current_encoding = current_encodings[0]
            print(f"🔐 Encoding gerado com sucesso! Tamanho: {len(current_encoding)}")
            
            # Comparar com embedding salvo
            saved_embedding = np.array(biometric.embedding)
            
            # Calcular distância euclidiana
            distance = np.linalg.norm(saved_embedding - current_encoding)
            threshold = 0.6  # Threshold padrão do face_recognition
            
            print(f"📊 Distância euclidiana: {distance:.4f} (threshold: {threshold})")
            
            if distance > threshold:
                print(f"❌ Face não reconhecida. Distância muito alta: {distance:.4f}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Face não reconhecida. Identidade não corresponde ao usuário {username}."
                )
            
            print(f"✅ Face reconhecida! Usuário: {username}")
            confidence = 1.0 - (distance / threshold)
            faces_detected = len(face_locations)
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Erro no reconhecimento facial: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro no processamento facial: {str(e)}"
            )
        
        # Gerar token
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": user.username,
            "role": user.role,
            "clearance": user.clearance,
            "confidence": confidence,
            "method": "facial_recognition" if confidence > 0.7 else "simplified_dev_mode",
            "faces_detected": faces_detected
        }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no login por câmera: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )


@router.post("/check-biometric")
async def check_biometric(body: dict, db: Session = Depends(get_db)):
    """
    Verifica se um usuário tem biometria cadastrada na tabela biometric_templates
    """
    try:
        username = body.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Username é obrigatório")
        
        from sqlalchemy import select
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Verificar se existe registro na tabela biometric_templates
        biometric = db.execute(
            select(BiometricTemplate).where(BiometricTemplate.user_id == user.id)
        ).scalar_one_or_none()
        
        has_biometric = biometric is not None
        
        return {
            "has_biometric": has_biometric,
            "message": "Biometria cadastrada" if has_biometric else "Biometria não cadastrada"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao verificar biometria: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")


@router.post("/login/upload")
async def login_by_upload(
    username: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Login via upload de imagem facial
    Similar ao login/camera, mas para imagens enviadas
    """
    # Reutilizar a mesma lógica do login por câmera
    return await login_by_camera(username, image, db)


@router.post("/enroll-upload")
async def enroll_biometric(
    username: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Cadastro de biometria facial via upload de imagem
    Usa face_recognition (dlib) para encoding facial
    """
    print(f"🔍 Recebendo requisição de cadastro para: {username}")
    print(f"📁 Arquivo: {image.filename}, Content-Type: {image.content_type}")
    
    try:
        # Verificar se usuário existe
        from sqlalchemy import select
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        
        if not user:
            print(f"❌ Usuário {username} não encontrado no banco")
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        print(f"✅ Usuário {username} encontrado (ID: {user.id})")
        
        # Ler e validar imagem
        contents = await image.read()
        print(f"📦 Tamanho da imagem: {len(contents)} bytes")
        
        img = Image.open(io.BytesIO(contents))
        print(f"🖼️ Imagem carregada: {img.size}, modo: {img.mode}")
        
        # Converter para RGB se necessário
        if img.mode != 'RGB':
            img = img.convert('RGB')
            print(f"🔄 Imagem convertida para RGB")
        
        # Converter para numpy array
        img_array = np.array(img)
        print(f"📐 Array shape: {img_array.shape}")
        
        print(f"🔐 Processando cadastro de biometria para {username}...")
        
        # Detectar faces usando face_recognition
        print(f"🔍 Detectando faces...")
        face_locations = face_recognition.face_locations(img_array)
        print(f"📍 {len(face_locations)} face(s) detectada(s)")
        
        if not face_locations or len(face_locations) == 0:
            raise HTTPException(
                status_code=400,
                detail="Nenhum rosto detectado na imagem. Use uma foto clara com seu rosto visível."
            )
        
        if len(face_locations) > 1:
            raise HTTPException(
                status_code=400,
                detail="Múltiplos rostos detectados. Use uma foto com apenas um rosto."
            )
        
        print(f"✅ Face detectada! Gerando encoding...")
        
        # Gerar encoding da face
        face_encodings = face_recognition.face_encodings(img_array, face_locations)
        
        if not face_encodings or len(face_encodings) == 0:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível processar a face detectada. Tente outra foto."
            )
        
        embedding = face_encodings[0].tolist()  # Converter para lista para salvar no banco
        print(f"✅ Encoding gerado! Tamanho: {len(embedding)}")
        
        # Verificar se já existe biometria cadastrada
        from sqlalchemy import select
        existing_biometric = db.execute(
            select(BiometricTemplate).where(BiometricTemplate.user_id == user.id)
        ).scalar_one_or_none()
        
        if existing_biometric:
            # Atualizar embedding existente
            existing_biometric.embedding = embedding
            print(f"🔄 Biometria atualizada para {username}")
        else:
            # Criar novo registro
            new_biometric = BiometricTemplate(
                user_id=user.id,
                embedding=embedding
            )
            db.add(new_biometric)
            print(f"✅ Biometria cadastrada para {username}")
        
        db.commit()
        
        return {
            "success": True,
            "message": "Biometria cadastrada com sucesso!",
            "username": username,
            "face_detected": True
        }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no cadastro de biometria para {username}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor: {str(e)}"
        )


# ===============================================
# ENDPOINTS DE CADASTRO DE USUÁRIOS
# ===============================================

class RegisterUserRequest(BaseModel):
    username: str
    password: str
    role: str = "public"  # public, director, minister
    clearance: int = 1  # 1, 2, ou 3

@router.post("/register")
def register_user(
    body: RegisterUserRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cadastrar novo usuário
    Requer autenticação (qualquer usuário logado pode cadastrar)
    """
    try:
        print(f"👤 Cadastro de novo usuário: {body.username} por {current_user['username']}")
        
        # Verificar se usuário já existe
        existing_user = db.execute(
            select(User).where(User.username == body.username)
        ).scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Usuário '{body.username}' já existe"
            )
        
        # Validar clearance
        if body.clearance not in [1, 2, 3]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Clearance deve ser 1, 2 ou 3"
            )
        
        # Validar role
        valid_roles = ["public", "director", "minister"]
        if body.role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role deve ser um de: {', '.join(valid_roles)}"
            )
        
        # Criar hash da senha
        password_hash = pwd_context.hash(body.password)
        
        # Criar novo usuário
        new_user = User(
            username=body.username,
            password_hash=password_hash,
            role=body.role,
            clearance=body.clearance
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"✅ Usuário '{body.username}' criado com sucesso!")
        
        return {
            "message": "Usuário cadastrado com sucesso",
            "user": {
                "username": new_user.username,
                "role": new_user.role,
                "clearance": new_user.clearance,
                "created_at": new_user.created_at.isoformat() if new_user.created_at else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao cadastrar usuário: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao cadastrar usuário: {str(e)}"
        )


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Listar todos os usuários
    Requer autenticação
    """
    try:
        users = db.execute(select(User)).scalars().all()
        
        return {
            "total": len(users),
            "users": [
                {
                    "username": user.username,
                    "role": user.role,
                    "clearance": user.clearance,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
                for user in users
            ]
        }
    except Exception as e:
        print(f"❌ Erro ao listar usuários: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao listar usuários"
        )


@router.delete("/users/{username}")
def delete_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Deletar usuário
    Requer autenticação
    Não permite deletar o próprio usuário
    """
    try:
        # Não permitir deletar a si mesmo
        if username == current_user['username']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você não pode deletar seu próprio usuário"
            )
        
        # Buscar usuário
        user = db.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário '{username}' não encontrado"
            )
        
        # Deletar biometrias associadas
        biometrics = db.execute(
            select(BiometricTemplate).where(BiometricTemplate.user_id == user.id)
        ).scalars().all()
        
        for bio in biometrics:
            db.delete(bio)
        
        # Deletar usuário
        db.delete(user)
        db.commit()
        
        print(f"✅ Usuário '{username}' deletado com sucesso!")
        
        return {
            "message": f"Usuário '{username}' deletado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao deletar usuário: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )


class ResetPasswordRequest(BaseModel):
    new_password: str


@router.put("/users/{username}/reset-password")
def reset_user_password(
    username: str,
    body: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Resetar senha de um usuário
    Requer autenticação
    """
    try:
        # Buscar usuário
        user = db.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário '{username}' não encontrado"
            )
        
        # Criar hash da nova senha
        new_password_hash = pwd_context.hash(body.new_password)
        
        # Atualizar senha
        user.password_hash = new_password_hash
        db.commit()
        
        print(f"✅ Senha do usuário '{username}' resetada com sucesso!")
        
        return {
            "message": f"Senha do usuário '{username}' resetada com sucesso",
            "username": username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao deletar usuário: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )
