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

from app.config import get_db, Base, engine
from app.models.user import User
from app.models.biometric_template import BiometricTemplate

router = APIRouter(prefix="/auth", tags=["auth"])

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# Lazy loading do DeepFace para economizar memória inicial
_deepface_loaded = False
DeepFace = None

def load_deepface():
    """Carrega DeepFace apenas quando necessário"""
    global _deepface_loaded, DeepFace
    if not _deepface_loaded:
        from deepface import DeepFace as DF
        DeepFace = DF
        _deepface_loaded = True
        print("✅ DeepFace carregado com sucesso")
    return DeepFace

# Create a demo user if DB is empty (only for first run / local tests)
from sqlalchemy import select
def _ensure_demo_user(db: Session):
    exists = db.execute(select(User).where(User.username == "ana.luiza")).scalar_one_or_none()
    if not exists:
        pwd = CryptContext(schemes=["bcrypt"], deprecated="auto").hash("admin123")
        db.add(User(username="ana.luiza", password=pwd))
        db.commit()

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
        # bootstrap demo user (safe for dev; remove in prod)
        _ensure_demo_user(db)

        from sqlalchemy import select
        user = db.execute(select(User).where(User.username == body.username)).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        if not pwd_context.verify(body.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta")

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

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
        print("Erro interno no /auth/login:", repr(e))
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


@router.post("/login/camera")
async def login_by_camera(
    username: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Login via reconhecimento facial usando câmera
    Usa DeepFace integrado para detecção e verificação facial
    """
    try:
        # Verificar se usuário existe
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Usar reconhecimento facial local com DeepFace
        print(f"🔍 Processando reconhecimento facial para usuário: {username}")
        
        # Carregar DeepFace
        df = load_deepface()
        
        # Ler imagem e converter para RGB
        image_bytes = await image.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        # Converter para RGB se necessário (remove canal alpha se existir)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            print(f"🔄 Imagem convertida de {img.mode} para RGB")
        
        img_array = np.array(img)
        print(f"📐 Shape da imagem: {img_array.shape}")
        
        # TODO: Implementar verificação real
        # Por enquanto, apenas verifica se há uma face detectada
        try:
            # Tentar detectar face
            faces = df.extract_faces(img_array, enforce_detection=True)
            
            if not faces or len(faces) == 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Nenhuma face detectada na imagem"
                )
            
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
            
            # Gerar embedding da imagem capturada
            print(f"🔐 Gerando embedding da imagem capturada...")
            try:
                current_embedding = df.represent(
                    img_path=img_array,
                    model_name='Facenet',
                    enforce_detection=True,
                    detector_backend='opencv'
                )
                print(f"✅ Embedding gerado com sucesso!")
            except Exception as embed_error:
                print(f"❌ Erro ao gerar embedding: {embed_error}")
                import traceback
                traceback.print_exc()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro ao processar imagem: {str(embed_error)}"
                )
            
            # Comparar embeddings usando distância euclidiana
            try:
                saved_embedding = np.array(biometric.embedding)
                current_embedding_array = np.array(current_embedding[0]['embedding'])
                
                print(f"🔢 Tamanho embedding salvo: {len(saved_embedding)}")
                print(f"🔢 Tamanho embedding atual: {len(current_embedding_array)}")
                print(f"🔢 Tipo embedding salvo: {type(biometric.embedding)}")
                
                distance = np.linalg.norm(saved_embedding - current_embedding_array)
                threshold = 10.0  # Threshold do Facenet (ajustável)
                
                print(f"📊 Distância euclidiana: {distance:.2f} (threshold: {threshold})")
                
                if distance > threshold:
                    print(f"❌ Face não reconhecida. Distância muito alta: {distance:.2f}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Face não reconhecida. Distância: {distance:.2f}"
                    )
                
                print(f"✅ Face reconhecida! Usuário: {username}")
            except HTTPException:
                raise
            except Exception as comp_error:
                print(f"❌ Erro na comparação: {comp_error}")
                import traceback
                traceback.print_exc()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro ao comparar biometria: {str(comp_error)}"
                )
            
            print(f"✅ Face reconhecida! Usuário: {username}")
            
            # Gerar token
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
            
            return {
                "access_token": token,
                "token_type": "bearer",
                "username": user.username,
                "role": user.role,
                "clearance": user.clearance,
                "confidence": 1.0 - (distance / threshold),  # Confiança baseada na distância
                "method": "local_deepface",
                "faces_detected": len(faces)
            }
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Erro na detecção facial: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no login por câmera: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Erro interno no servidor"
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
    """
    try:
        # Verificar se usuário existe
        from sqlalchemy import select
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Ler e validar imagem
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # Converter para RGB se necessário
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Carregar DeepFace
        df = load_deepface()
        
        # Converter para numpy array
        img_array = np.array(img)
        
        # Validar que há um rosto na imagem
        try:
            faces = df.extract_faces(
                img_path=img_array,
                detector_backend='opencv',
                enforce_detection=True
            )
            
            if not faces or len(faces) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Nenhum rosto detectado na imagem. Use uma foto clara com seu rosto visível."
                )
            
            if len(faces) > 1:
                raise HTTPException(
                    status_code=400,
                    detail="Múltiplos rostos detectados. Use uma foto com apenas um rosto."
                )
            
            # Gerar embedding da face
            print(f"🔐 Gerando embedding facial para {username}...")
            embedding = df.represent(
                img_path=img_array,
                model_name='Facenet',
                enforce_detection=True,
                detector_backend='opencv'
            )
            
            # Verificar se já existe biometria cadastrada
            from sqlalchemy import select
            existing_biometric = db.execute(
                select(BiometricTemplate).where(BiometricTemplate.user_id == user.id)
            ).scalar_one_or_none()
            
            if existing_biometric:
                # Atualizar embedding existente
                existing_biometric.embedding = embedding[0]['embedding']
                print(f"🔄 Biometria atualizada para {username}")
            else:
                # Criar novo registro
                new_biometric = BiometricTemplate(
                    user_id=user.id,
                    embedding=embedding[0]['embedding']
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
            
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erro na detecção facial: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no cadastro de biometria: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Erro interno no servidor"
        )
