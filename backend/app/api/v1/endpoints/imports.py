from typing import Any, Dict
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.import_service import ImportService
from app.services.audit_service import AuditService
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.post("/csv")
async def import_inventory_csv(
    facility_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to specified facility")

    content = await file.read()
    try:
        decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        decoded_content = content.decode("latin-1")

    service = ImportService(db)
    result = service.parse_and_import_csv(decoded_content, facility_id=facility_id)

    AuditService.log_action(
        db,
        action="INVENTORY_CSV_IMPORT",
        entity_type="Facility",
        user_id=current_user.id,
        entity_id=str(facility_id),
        details={"filename": file.filename, "imported_count": result.get("imported_count")},
    )

    return result
