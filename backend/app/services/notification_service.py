"""
PharmaIntelligence AI - Clinical Supply Chain Notification Service

Aggregates real-time alerts from:
1. Stockout Risk: Facilities with critically low Days of Stock Remaining (DSR < 1.0) or high stockout probability
2. Impending Expiry: Batches expiring within 90 days with surplus beyond projected consumption
3. Redistribution Recommendations: Pending lateral transfer proposals awaiting pharmacist/director approval
4. Data Quality: Facilities with flagged stock reconciliation anomalies or high missingness
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.facility import Facility
from app.models.inventory import Inventory
from app.models.batch import Batch
from app.models.medicine import Medicine
from app.models.recommendation import RedistributionRecommendation
from app.models.data_quality import DataQualityIssue


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def get_active_notifications(
        self,
        facility_id: Optional[int] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        notifications: List[Dict[str, Any]] = []

        # 1. Critical Stockout Alerts (months_of_stock < 0.5 or stock_status in ["Stockout", "Understocked"])
        inv_query = self.db.query(Inventory, Medicine, Facility).join(
            Medicine, Inventory.medicine_id == Medicine.id
        ).join(
            Facility, Inventory.facility_id == Facility.id
        ).filter(
            (Inventory.months_of_stock < 0.5) | (Inventory.stock_status.in_(["Stockout", "Understocked"]))
        )
        if facility_id:
            inv_query = inv_query.filter(Inventory.facility_id == facility_id)

        low_stock_items = inv_query.limit(10).all()
        for inv, med, fac in low_stock_items:
            mos = inv.months_of_stock or 0.0
            dsr = mos * 30.0
            severity = "critical" if (inv.usable_stock <= 0 or mos < 0.2) else "high"
            notifications.append({
                "id": f"notif-stockout-{inv.id}",
                "title": f"Stockout Risk: {med.name} ({med.strength or ''})",
                "message": f"Stock at {fac.name} has fallen to {inv.usable_stock:.0f} {med.unit_of_measure} ({dsr:.1f} Days of Supply Remaining / {mos:.1f} MOS). Immediate replenishment or lateral transfer advised.",
                "severity": severity,
                "timestamp": inv.updated_at.isoformat() if hasattr(inv, 'updated_at') and inv.updated_at else datetime.now(timezone.utc).isoformat(),
                "facility": fac.name,
                "category": "Stockout",
                "isRead": False,
                "actionUrl": "/stockout-intelligence",
            })

        # 2. Expiry Risk Alerts (Batches expiring within 90 days)
        now_date = datetime.now(timezone.utc).date()
        batch_query = self.db.query(Batch, Medicine, Facility).join(
            Medicine, Batch.medicine_id == Medicine.id
        ).join(
            Facility, Batch.facility_id == Facility.id
        ).filter(
            Batch.quantity_remaining > 0,
        )
        if facility_id:
            batch_query = batch_query.filter(Batch.facility_id == facility_id)

        all_batches = batch_query.limit(20).all()
        for batch, med, fac in all_batches:
            days = (batch.expiry_date - now_date).days if batch.expiry_date else 999
            if days < 90:
                severity = "critical" if days < 30 else "high"
                notifications.append({
                    "id": f"notif-expiry-{batch.id}",
                    "title": f"Impending Expiry: Batch {batch.batch_number}",
                    "message": f"{batch.quantity_remaining:.0f} units of {med.name} at {fac.name} will expire in {days} days ({batch.expiry_date.strftime('%Y-%m-%d')}). Consider FEFO lateral transfer.",
                    "severity": severity,
                    "timestamp": batch.created_at.isoformat() if hasattr(batch, 'created_at') and batch.created_at else datetime.now(timezone.utc).isoformat(),
                    "facility": fac.name,
                    "category": "Expiry",
                    "isRead": False,
                    "actionUrl": "/expiry-prevention",
                })

        # 3. Pending Redistribution Proposals
        rec_query = self.db.query(
            RedistributionRecommendation, Medicine, Facility
        ).join(
            Medicine, RedistributionRecommendation.medicine_id == Medicine.id
        ).join(
            Facility, RedistributionRecommendation.source_facility_id == Facility.id
        ).filter(
            RedistributionRecommendation.status == "PENDING"
        )
        if facility_id:
            rec_query = rec_query.filter(
                (RedistributionRecommendation.source_facility_id == facility_id) |
                (RedistributionRecommendation.destination_facility_id == facility_id)
            )

        pending_recs = rec_query.limit(10).all()
        for rec, med, source_fac in pending_recs:
            dest_fac = self.db.get(Facility, rec.destination_facility_id)
            dest_name = dest_fac.name if dest_fac else f"Facility #{rec.destination_facility_id}"
            notifications.append({
                "id": f"notif-redist-{rec.id}",
                "title": f"Lateral Transfer Pending: {med.name}",
                "message": f"MILP Solver proposed transfer of {rec.quantity_recommended:.0f} units from {source_fac.name} to {dest_name} (Est. ETB {rec.prevented_wastage_cost_etb or 0:,.0f} saved).",
                "severity": "medium",
                "timestamp": rec.created_at.isoformat() if rec.created_at else datetime.now(timezone.utc).isoformat(),
                "facility": source_fac.name,
                "category": "Redistribution",
                "isRead": False,
                "actionUrl": "/redistribution",
            })

        # 4. Data Quality Reconciliation Issues
        dq_query = self.db.query(DataQualityIssue, Facility).join(
            Facility, DataQualityIssue.facility_id == Facility.id
        ).filter(
            DataQualityIssue.is_resolved == False
        )
        if facility_id:
            dq_query = dq_query.filter(DataQualityIssue.facility_id == facility_id)

        dq_issues = dq_query.limit(5).all()
        for issue, fac in dq_issues:
            notifications.append({
                "id": f"notif-dq-{issue.id}",
                "title": f"Data Quality Issue: {issue.dimension.value if hasattr(issue.dimension, 'value') else issue.dimension}",
                "message": f"{fac.name}: {issue.description or 'Unresolved discrepancy in inventory records.'}",
                "severity": "medium",
                "timestamp": issue.detected_at.isoformat() if issue.detected_at else datetime.now(timezone.utc).isoformat(),
                "facility": fac.name,
                "category": "Quality",
                "isRead": False,
                "actionUrl": "/data-quality",
            })

        # Sort: critical first, then high, then medium, then by timestamp
        priority_order = {"critical": 0, "high": 1, "medium": 2, "info": 3}
        notifications.sort(key=lambda n: (priority_order.get(n["severity"], 4), n["timestamp"]), reverse=False)

        return notifications[:limit]
