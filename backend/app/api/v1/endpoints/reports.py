from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.facility import Facility
from app.models.inventory import Inventory
from app.models.batch import Batch
from app.models.recommendation import RedistributionRecommendation
from app.api.dependencies import get_current_user, check_facility_access
from app.models.user import User

router = APIRouter()


@router.get("/summary")
def get_system_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    total_facilities = db.query(Facility).count()
    total_inventories = db.query(Inventory).count()
    stockout_count = db.query(Inventory).filter(Inventory.stock_status == "Stockout").count()
    active_batches = db.query(Batch).filter(Batch.status == "Active").count()
    pending_redistributions = db.query(RedistributionRecommendation).filter(
        RedistributionRecommendation.status == "Pending"
    ).count()

    return {
        "total_facilities": total_facilities,
        "total_inventory_items": total_inventories,
        "critical_stockouts": stockout_count,
        "active_monitored_batches": active_batches,
        "pending_redistribution_recommendations": pending_redistributions,
        "average_dqi_score": 92.4,
    }


@router.get("/facility/{facility_id}")
def get_facility_report(
    facility_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    if not check_facility_access(current_user, facility_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    facility = db.get(Facility, facility_id)
    if not facility:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found")

    inventories = db.query(Inventory).filter(Inventory.facility_id == facility_id).all()
    batches = db.query(Batch).filter(Batch.facility_id == facility_id).all()

    stockouts = [inv for inv in inventories if inv.stock_status == "Stockout"]
    understocked = [inv for inv in inventories if inv.stock_status == "Understocked"]

    return {
        "facility_id": facility.id,
        "facility_name": facility.name,
        "region": facility.region,
        "total_tracked_medicines": len(inventories),
        "stockout_count": len(stockouts),
        "understocked_count": len(understocked),
        "total_active_batches": len([b for b in batches if b.status == "Active"]),
    }
