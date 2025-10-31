"""Sistema de auditoria: logs de acesso e ações do sistema"""

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Request
from ..models import AuditLog


def log_action(
    db: Session,
    user: str,
    action: str,
    level_requested: Optional[int] = None,
    success: bool = True,
    origin_ip: Optional[str] = None,
    details: Optional[str] = None
) -> AuditLog:
    """
    Registra uma ação no sistema de auditoria.
    
    Args:
        db: Sessão do banco de dados
        user: Nome do usuário que executou a ação
        action: Tipo de ação (LOGIN, DATA_ACCESS, ENROLL, etc.)
        level_requested: Nível de dados solicitado (1, 2 ou 3)
        success: Se a ação foi bem-sucedida
        origin_ip: IP de origem da requisição
        details: Informações adicionais sobre a ação
    
    Returns:
        Registro de auditoria criado
    """
    audit_log = AuditLog(
        user=user,
        action=action,
        level_requested=level_requested,
        success=success,
        origin_ip=origin_ip,
        details=details,
        timestamp=datetime.utcnow()
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    
    return audit_log


def log_login_attempt(
    db: Session,
    username: str,
    success: bool,
    request: Request,
    failure_reason: Optional[str] = None
) -> AuditLog:
    """
    Registra tentativa de login (sucesso ou falha).
    """
    client_ip = request.client.host if request.client else "unknown"
    
    details = None
    if not success and failure_reason:
        details = f"Falha no login: {failure_reason}"
    
    return log_action(
        db=db,
        user=username,
        action="LOGIN_ATTEMPT",
        success=success,
        origin_ip=client_ip,
        details=details
    )


def log_data_access(
    db: Session,
    username: str,
    level_requested: int,
    success: bool,
    request: Request,
    data_type: Optional[str] = None
) -> AuditLog:
    """
    Registra acesso a dados por nível de clearance.
    """
    client_ip = request.client.host if request.client else "unknown"
    
    details = None
    if data_type:
        details = f"Acesso a dados: {data_type}"
    
    return log_action(
        db=db,
        user=username,
        action="DATA_ACCESS",
        level_requested=level_requested,
        success=success,
        origin_ip=client_ip,
        details=details
    )


def log_biometric_enroll(
    db: Session,
    username: str,
    success: bool,
    request: Request,
    details: Optional[str] = None
) -> AuditLog:
    """
    Registra tentativa de cadastro biométrico.
    """
    client_ip = request.client.host if request.client else "unknown"
    
    return log_action(
        db=db,
        user=username,
        action="BIOMETRIC_ENROLL",
        success=success,
        origin_ip=client_ip,
        details=details
    )


def log_security_event(
    db: Session,
    username: str,
    event_type: str,
    request: Request,
    details: str
) -> AuditLog:
    """
    Registra eventos de segurança (tentativas de acesso não autorizado, etc.).
    """
    client_ip = request.client.host if request.client else "unknown"
    
    return log_action(
        db=db,
        user=username,
        action=f"SECURITY_{event_type}",
        success=False,  # Eventos de segurança são geralmente falhas
        origin_ip=client_ip,
        details=details
    )


def get_audit_statistics(db: Session, days: int = 30) -> dict:
    """
    Retorna estatísticas de auditoria dos últimos N dias.
    """
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Total de ações
    total_actions = db.query(AuditLog).filter(
        AuditLog.timestamp >= cutoff_date
    ).count()
    
    # Ações por sucesso
    successful_actions = db.query(AuditLog).filter(
        AuditLog.timestamp >= cutoff_date,
        AuditLog.success == True
    ).count()
    
    failed_actions = total_actions - successful_actions
    
    # Ações por tipo
    login_attempts = db.query(AuditLog).filter(
        AuditLog.timestamp >= cutoff_date,
        AuditLog.action == "LOGIN_ATTEMPT"
    ).count()
    
    data_accesses = db.query(AuditLog).filter(
        AuditLog.timestamp >= cutoff_date,
        AuditLog.action == "DATA_ACCESS"
    ).count()
    
    # Acessos por nível
    level_1_access = db.query(AuditLog).filter(
        AuditLog.timestamp >= cutoff_date,
        AuditLog.level_requested == 1,
        AuditLog.success == True
    ).count()
    
    level_2_access = db.query(AuditLog).filter(
        AuditLog.timestamp >= cutoff_date,
        AuditLog.level_requested == 2,
        AuditLog.success == True
    ).count()
    
    level_3_access = db.query(AuditLog).filter(
        AuditLog.timestamp >= cutoff_date,
        AuditLog.level_requested == 3,
        AuditLog.success == True
    ).count()
    
    return {
        "period_days": days,
        "total_actions": total_actions,
        "successful_actions": successful_actions,
        "failed_actions": failed_actions,
        "success_rate": round((successful_actions / total_actions * 100) if total_actions > 0 else 0, 2),
        "action_types": {
            "login_attempts": login_attempts,
            "data_accesses": data_accesses
        },
        "level_access": {
            "level_1": level_1_access,
            "level_2": level_2_access,
            "level_3": level_3_access
        }
    }

from sqlalchemy.orm import Session
from ..models import AuditLog
from typing import Optional


def log_action(
    db: Session,
    user: str,
    action: str,
    success: bool,
    level_requested: int = 0,
    origin_ip: Optional[str] = None
):
    """
    Registra uma ação no log de auditoria.
    
    Args:
        db: Sessão do banco de dados
        user: Nome do usuário que realizou a ação
        action: Tipo de ação (enroll, verify, access_level_X)
        success: Se a ação foi bem-sucedida
        level_requested: Nível de clearance solicitado (para acessos a dados)
        origin_ip: IP de origem da requisição
    """
    log = AuditLog(
        user=user,
        action=action,
        level_requested=level_requested,
        success=success,
        origin_ip=origin_ip
    )
    db.add(log)
    db.commit()
