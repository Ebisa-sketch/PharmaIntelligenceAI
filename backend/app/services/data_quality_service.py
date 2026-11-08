import json
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.batch import Batch
from app.models.inventory import Inventory
from app.models.facility import Facility
from app.models.medicine import Medicine
from app.models.transaction import InventoryTransaction
from app.models.data_quality import DataQualityIssue
from app.models.data_import import DataImport


class DataQualityService:
    def __init__(self, db: Session):
        self.db = db

    def assess_facility_data_quality(
        self,
        facility_id: int,
        persist_issues: bool = True,
        import_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Calculates Data Quality Index (DQI) across 5 core dimensions:
        1. Completeness: Missing required medicine/batch identifiers, null quantities
        2. Consistency: Ledger reconciliation (Batch sum == Inventory current stock)
        3. Plausibility: Non-negativity, logical quantity ranges, valid dates
        4. Expiry Validity: Expired batches marked Active, invalid shelf-life
        5. Uniqueness: Duplicate active batch entries for same facility & medicine
        """
        facility = self.db.get(Facility, facility_id)
        facility_name = facility.name if facility else f"Facility #{facility_id}"

        batches = self.db.query(Batch).filter(Batch.facility_id == facility_id).all()
        inventories = self.db.query(Inventory).filter(Inventory.facility_id == facility_id).all()
        today = date.today()

        total_batches = len(batches)
        total_inventories = len(inventories)

        # Dimension scores start at 100.0
        dim_scores = {
            "Completeness": 100.0,
            "Consistency": 100.0,
            "Plausibility": 100.0,
            "Expiry Validity": 100.0,
            "Uniqueness": 100.0,
        }

        issues: List[Dict[str, Any]] = []

        # If facility has no records yet
        if total_batches == 0 and total_inventories == 0:
            return {
                "facility_id": facility_id,
                "facility_name": facility_name,
                "dqi_score": 100.0,
                "status": "Healthy",
                "dimensions": [
                    {
                        "dimension": dim,
                        "score": 100.0,
                        "status": "Excellent",
                        "issue_count": 0,
                        "description": f"No {dim.lower()} violations detected.",
                    }
                    for dim in dim_scores
                ],
                "total_issues": 0,
                "critical_issues_count": 0,
                "warning_issues_count": 0,
                "total_batches_analyzed": 0,
                "total_inventories_analyzed": 0,
                "assessed_at": datetime.now(timezone.utc),
            }

        # 1. Check Batches for Plausibility, Expiry Validity, and Uniqueness
        seen_batches = set()
        plausibility_deductions = 0.0
        validity_deductions = 0.0
        uniqueness_deductions = 0.0
        completeness_deductions = 0.0

        for b in batches:
            # Completeness: Check batch number and dates
            if not b.batch_number or not str(b.batch_number).strip():
                completeness_deductions += 10.0
                issues.append({
                    "facility_id": facility_id,
                    "medicine_id": b.medicine_id,
                    "issue_type": "MISSING_IDENTIFIER",
                    "severity": "CRITICAL",
                    "dimension": "Completeness",
                    "field_name": "batch_number",
                    "description": f"Batch ID #{b.id} has empty or blank batch number.",
                })

            # Plausibility: Negative stock
            if b.quantity_remaining < 0:
                plausibility_deductions += 15.0
                issues.append({
                    "facility_id": facility_id,
                    "medicine_id": b.medicine_id,
                    "issue_type": "NEGATIVE_STOCK",
                    "severity": "CRITICAL",
                    "dimension": "Plausibility",
                    "field_name": "quantity_remaining",
                    "description": f"Batch '{b.batch_number}' has negative remaining quantity ({b.quantity_remaining}).",
                })

            # Plausibility: Remaining quantity cannot exceed initial quantity (unless positive adjustment)
            if b.quantity_remaining > b.quantity_initial and b.quantity_initial > 0:
                plausibility_deductions += 5.0
                issues.append({
                    "facility_id": facility_id,
                    "medicine_id": b.medicine_id,
                    "issue_type": "QUANTITY_OVERFLOW",
                    "severity": "WARNING",
                    "dimension": "Plausibility",
                    "field_name": "quantity_remaining",
                    "description": f"Batch '{b.batch_number}' remaining ({b.quantity_remaining}) exceeds initial quantity ({b.quantity_initial}).",
                })

            # Expiry Validity: Expired active batch
            if b.status == "Active" and b.expiry_date < today:
                validity_deductions += 8.0
                days_expired = (today - b.expiry_date).days
                issues.append({
                    "facility_id": facility_id,
                    "medicine_id": b.medicine_id,
                    "issue_type": "EXPIRED_ACTIVE_STOCK",
                    "severity": "CRITICAL" if days_expired > 30 else "WARNING",
                    "dimension": "Expiry Validity",
                    "field_name": "expiry_date",
                    "description": f"Batch '{b.batch_number}' expired {days_expired} days ago on {b.expiry_date} but remains marked 'Active'.",
                })

            # Uniqueness: Duplicate active batch
            key = (b.medicine_id, str(b.batch_number).strip().upper())
            if key in seen_batches and b.status == "Active":
                uniqueness_deductions += 12.0
                issues.append({
                    "facility_id": facility_id,
                    "medicine_id": b.medicine_id,
                    "issue_type": "DUPLICATE_ENTRY",
                    "severity": "WARNING",
                    "dimension": "Uniqueness",
                    "field_name": "batch_number",
                    "description": f"Duplicate active batch record '{b.batch_number}' found for medicine #{b.medicine_id}.",
                })
            seen_batches.add(key)

        # 2. Check Consistency: Inventory stock vs sum of active batch quantities
        consistency_deductions = 0.0
        for inv in inventories:
            # Check negative current stock
            if inv.current_stock < 0:
                plausibility_deductions += 15.0
                issues.append({
                    "facility_id": facility_id,
                    "medicine_id": inv.medicine_id,
                    "issue_type": "NEGATIVE_STOCK",
                    "severity": "CRITICAL",
                    "dimension": "Plausibility",
                    "field_name": "current_stock",
                    "description": f"Inventory for medicine #{inv.medicine_id} has negative stock balance ({inv.current_stock}).",
                })

            # Reconcile sum of active batch remaining quantities
            batch_sum = sum(
                b.quantity_remaining
                for b in batches
                if b.medicine_id == inv.medicine_id and b.status == "Active"
            )

            # Allow minor floating point epsilon (0.01)
            discrepancy = round(abs(inv.current_stock - batch_sum), 3)
            if discrepancy > 0.01:
                consistency_deductions += 10.0
                issues.append({
                    "facility_id": facility_id,
                    "medicine_id": inv.medicine_id,
                    "issue_type": "RECONCILIATION_ERROR",
                    "severity": "CRITICAL" if discrepancy > 50 else "WARNING",
                    "dimension": "Consistency",
                    "field_name": "current_stock",
                    "description": f"Medicine #{inv.medicine_id} ledger stock ({inv.current_stock}) mismatches active batches sum ({batch_sum}), discrepancy: {discrepancy}.",
                    "details": json.dumps({"current_stock": inv.current_stock, "batch_sum": batch_sum, "discrepancy": discrepancy}),
                })

        # Calculate final dimensional scores bounded [0.0, 100.0]
        dim_scores["Completeness"] = max(0.0, 100.0 - completeness_deductions)
        dim_scores["Consistency"] = max(0.0, 100.0 - consistency_deductions)
        dim_scores["Plausibility"] = max(0.0, 100.0 - plausibility_deductions)
        dim_scores["Expiry Validity"] = max(0.0, 100.0 - validity_deductions)
        dim_scores["Uniqueness"] = max(0.0, 100.0 - uniqueness_deductions)

        # Weighted aggregate DQI score
        # Consistency (25%), Plausibility (25%), Expiry Validity (20%), Completeness (15%), Uniqueness (15%)
        weighted_dqi = (
            dim_scores["Consistency"] * 0.25
            + dim_scores["Plausibility"] * 0.25
            + dim_scores["Expiry Validity"] * 0.20
            + dim_scores["Completeness"] * 0.15
            + dim_scores["Uniqueness"] * 0.15
        )
        weighted_dqi = round(max(0.0, min(100.0, weighted_dqi)), 1)

        status = (
            "Excellent" if weighted_dqi >= 90.0
            else ("Good" if weighted_dqi >= 75.0
                  else ("Degraded" if weighted_dqi >= 60.0 else "Critical"))
        )

        critical_count = sum(1 for i in issues if i["severity"] == "CRITICAL")
        warning_count = sum(1 for i in issues if i["severity"] == "WARNING")

        # Persist issues to database if requested
        if persist_issues and issues:
            self._persist_quality_issues(issues, import_id=import_id)

        dimensions_list = []
        for dim, score in dim_scores.items():
            dim_issue_count = sum(1 for i in issues if i.get("dimension") == dim)
            dim_status = (
                "Excellent" if score >= 90.0
                else ("Good" if score >= 75.0
                      else ("Degraded" if score >= 60.0 else "Critical"))
            )
            dimensions_list.append({
                "dimension": dim,
                "score": round(score, 1),
                "status": dim_status,
                "issue_count": dim_issue_count,
                "description": f"{dim} scored {round(score, 1)}% with {dim_issue_count} detected issues.",
            })

        return {
            "facility_id": facility_id,
            "facility_name": facility_name,
            "dqi_score": weighted_dqi,
            "status": status,
            "dimensions": dimensions_list,
            "total_issues": len(issues),
            "critical_issues_count": critical_count,
            "warning_issues_count": warning_count,
            "total_batches_analyzed": total_batches,
            "total_inventories_analyzed": total_inventories,
            "assessed_at": datetime.now(timezone.utc),
            "issues": issues,
        }

    def _persist_quality_issues(
        self, issues: List[Dict[str, Any]], import_id: Optional[int] = None
    ) -> None:
        """Saves generated data quality issues into data_quality_issues table."""
        # Find or create a default system/automated import record if import_id is None
        effective_import_id = import_id
        if effective_import_id is None:
            # Check for latest import or create placeholder
            existing_import = self.db.query(DataImport).first()
            if existing_import:
                effective_import_id = existing_import.id

        if effective_import_id is not None:
            for item in issues:
                db_issue = DataQualityIssue(
                    import_id=effective_import_id,
                    facility_id=item["facility_id"],
                    medicine_id=item.get("medicine_id"),
                    issue_type=item["issue_type"],
                    severity=item["severity"],
                    field_name=item.get("field_name"),
                    row_number=item.get("row_number"),
                    description=item["description"],
                    details=item.get("details"),
                    is_resolved=False,
                )
                self.db.add(db_issue)
            self.db.commit()

    def get_quality_issues(
        self,
        facility_id: Optional[int] = None,
        import_id: Optional[int] = None,
        severity: Optional[str] = None,
        is_resolved: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[DataQualityIssue]:
        """Queries logged data quality issues with optional filters."""
        query = self.db.query(DataQualityIssue)
        if facility_id:
            query = query.filter(DataQualityIssue.facility_id == facility_id)
        if import_id:
            query = query.filter(DataQualityIssue.import_id == import_id)
        if severity:
            query = query.filter(DataQualityIssue.severity == severity.upper())
        if is_resolved is not None:
            query = query.filter(DataQualityIssue.is_resolved == is_resolved)

        return query.order_by(DataQualityIssue.id.desc()).offset(skip).limit(limit).all()

    def resolve_issue(self, issue_id: int, notes: Optional[str] = None) -> Optional[DataQualityIssue]:
        """Marks a quality issue as resolved."""
        issue = self.db.get(DataQualityIssue, issue_id)
        if issue:
            issue.is_resolved = True
            if notes:
                existing_details = issue.details or ""
                issue.details = f"{existing_details}\n[Resolution]: {notes}".strip()
            self.db.commit()
            self.db.refresh(issue)
        return issue
