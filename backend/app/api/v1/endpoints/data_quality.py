from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.data_quality_service import DataQualityService
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.get("/facilities/{facility_id}")
def get_facility_data_quality(
    facility_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to requested facility")

    service = DataQualityService(db)
    return service.assess_facility_data_quality(facility_id)
