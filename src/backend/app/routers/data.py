from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/ping")
def ping():
    return {"pong": True}

@router.get("/level/{level}")
async def get_level_data(
    level: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna dados do nível de acesso especificado.
    Usuário precisa ter clearance >= level para acessar.
    """
    # Buscar usuário no banco para obter clearance
    from sqlalchemy import select
    user = db.execute(select(User).where(User.username == current_user["username"])).scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar permissão
    if user.clearance < level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acesso negado. Você precisa de clearance nível {level} ou superior."
        )
    
    # Dados mock por nível
    data_by_level = {
        1: {
            "level": 1,
            "title": "Nível 1 - Público",
            "description": "Informações básicas do sistema",
            "items": [
                {"id": 1, "name": "Documento A", "type": "public", "access": "Público"},
                {"id": 2, "name": "Manual Básico", "type": "public", "access": "Público"},
                {"id": 3, "name": "FAQ Geral", "type": "public", "access": "Público"}
            ]
        },
        2: {
            "level": 2,
            "title": "Nível 2 - Diretor",
            "description": "Relatórios gerenciais e estatísticas",
            "items": [
                {"id": 4, "name": "Relatório Mensal", "type": "confidential", "access": "Diretor"},
                {"id": 5, "name": "Dashboard Analytics", "type": "confidential", "access": "Diretor"},
                {"id": 6, "name": "Métricas de Performance", "type": "confidential", "access": "Diretor"}
            ]
        },
        3: {
            "level": 3,
            "title": "Nível 3 - Ministro",
            "description": "Documentos estratégicos e confidenciais",
            "items": [
                {"id": 7, "name": "Estratégia Nacional", "type": "top-secret", "access": "Ministro"},
                {"id": 8, "name": "Orçamento Secreto", "type": "top-secret", "access": "Ministro"},
                {"id": 9, "name": "Plano Quinquenal", "type": "top-secret", "access": "Ministro"}
            ]
        }
    }
    
    if level not in data_by_level:
        raise HTTPException(status_code=404, detail="Nível não encontrado")
    
    return {
        "success": True,
        "user_clearance": user.clearance,
        "requested_level": level,
        "data": data_by_level[level]
    }
