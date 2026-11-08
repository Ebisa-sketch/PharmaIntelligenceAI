from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.audit_log import AuditLog
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/")
def list_audit_logs(
    action: Optional[str] = None,
    entity_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    stmt = select(AuditLog)
    if action:
        stmt = stmt.where(AuditLog.action == action)
    if entity_type:
        stmt = stmt.where(AuditLog.entity_type == entity_type)
    stmt = stmt.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit)
    logs = db.scalars(stmt).all()

    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "timestamp": log.timestamp.isoformat(),
        }
        for log in logs
    ]
