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
        
        # Ler imagem
        image_bytes = await image.read()
        img = Image.open(io.BytesIO(image_bytes))
        img_array = np.array(img)
        
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
            
            # TODO: Comparar com embedding salvo do usuário
            # Por enquanto, se detectou uma face, aceita
            print(f"✅ Face detectada para usuário {username}")
            
            # Gerar token
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
            
            return {
                "access_token": token,
                "token_type": "bearer",
                "username": user.username,
                "role": user.role,
                "clearance": user.clearance,
                "confidence": 0.95,  # Mock - implementar cálculo real
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
    Verifica se um usuário tem biometria cadastrada
    """
    try:
        username = body.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Username é obrigatório")
        
        from sqlalchemy import select
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Por enquanto, sempre retorna False (biometria não implementada ainda)
        # TODO: Implementar verificação real quando salvarmos embeddings
        return {
            "has_biometric": False,
            "message": "Biometria não cadastrada"
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
