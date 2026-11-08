import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        action: str,
        entity_type: str,
        user_id: Optional[int] = None,
        entity_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        details_str = json.dumps(details, default=str) if details else None
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details_str,
            ip_address=ip_address,
            timestamp=datetime.now(timezone.utc),
        )
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        return audit_entry
