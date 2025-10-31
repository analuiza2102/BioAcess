"""Rotas de relatórios e auditoria (apenas clearance 3)"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import Optional
from ..db import get_db
from ..models import User, AuditLog
from ..security import require_level

router = APIRouter(prefix="/reports", tags=["relatórios"])


@router.get("/audit")
async def get_audit_logs(
    request: Request,
    page: int = Query(1, ge=1, description="Página atual"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    start_date: Optional[str] = Query(None, description="Data inicial (ISO format)"),
    end_date: Optional[str] = Query(None, description="Data final (ISO format)"),
    action: Optional[str] = Query(None, description="Filtrar por tipo de ação"),
    success: Optional[bool] = Query(None, description="Filtrar por sucesso/falha"),
    user: User = Depends(require_level(3)),  # apenas clearance 3 (ministro)
    db: Session = Depends(get_db)
):
    """
    Retorna logs de auditoria com filtros e paginação.
    
    Apenas usuários com clearance 3 (ministro) podem acessar.
    
    Query params:
        - page: Página atual (padrão: 1)
        - limit: Itens por página (padrão: 10, max: 100)
        - start_date: Data inicial (formato ISO)
        - end_date: Data final (formato ISO)
        - action: Filtrar por ação (enroll, verify, access_level_X)
        - success: Filtrar por sucesso (true/false)
    
    Returns:
        - logs: Lista de logs
        - total: Total de registros
        - page: Página atual
        - limit: Itens por página
    """
    query = db.query(AuditLog)
    
    # Aplica filtros dinamicamente
    filters = []
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            filters.append(AuditLog.ts >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            filters.append(AuditLog.ts <= end)
        except ValueError:
            pass
    
    if action:
        filters.append(AuditLog.action.ilike(f"%{action}%"))
    
    if success is not None:
        filters.append(AuditLog.success == success)
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Conta total antes da paginação
    total = query.count()
    
    # Aplica paginação e ordenação
    offset = (page - 1) * limit
    logs = query.order_by(AuditLog.ts.desc()).offset(offset).limit(limit).all()
    
    return {
        "logs": [
            {
                "id": log.id,
                "user": log.user,
                "action": log.action,
                "level_requested": log.level_requested,
                "success": log.success,
                "origin_ip": log.origin_ip,
                "ts": log.ts.isoformat()
            }
            for log in logs
        ],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 0
    }
