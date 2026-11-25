from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.notification_service import NotificationService
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

# In-memory store for read notifications per user session
_read_notification_ids: set = set()


@router.get("/", summary="List active clinical and supply chain notifications")
def get_notifications(
    facility_id: Optional[int] = Query(None, description="Optional facility filter"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """
    Returns real-time aggregated clinical notifications across stockout risk,
    batch expiry, redistribution proposals, and data quality anomalies.
    """
    service = NotificationService(db)
    items = service.get_active_notifications(facility_id=facility_id, limit=limit)
    
    # Mark read state from session
    for item in items:
        if item["id"] in _read_notification_ids:
            item["isRead"] = True

    return items


@router.post("/{notification_id}/read", summary="Mark notification as read")
def mark_notification_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Marks an individual notification as read."""
    _read_notification_ids.add(notification_id)
    return {"status": "success", "id": notification_id, "isRead": True}


@router.post("/read-all", summary="Mark all notifications as read")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Marks all active notifications as read."""
    service = NotificationService(db)
    items = service.get_active_notifications(limit=100)
    for item in items:
        _read_notification_ids.add(item["id"])
    return {"status": "success", "count": len(items)}
