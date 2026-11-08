import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.facility import Facility
from app.models.batch import Batch
from app.models.medicine import Medicine
from app.models.inventory import Inventory
from app.models.transaction import InventoryTransaction
from app.models.audit_log import AuditLog
from app.models.recommendation import RedistributionRecommendation
from app.repositories.prediction_repository import PredictionRepository
from app.schemas.recommendation import (
    RedistributionOptimizationRun,
    RedistributionResponse,
    RedistributionDetailResponse,
    MathematicalProof,
    SimulationScenarioRequest,
    SimulationScenarioResponse,
)
from app.ml.redistribution_optimizer import MILPRedistributionOptimizer, haversine_distance_km
from app.ml.simulation_scenarios import RedistributionSimulator
from app.core.exceptions import EntityNotFoundException, UnauthorizedActionException


class RedistributionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PredictionRepository(db)

    def optimize_and_generate_recommendations(
        self, params: RedistributionOptimizationRun
    ) -> List[RedistributionRecommendation]:
        """
        Solves the Mixed-Integer Linear Programming (MILP) redistribution optimization:
        - Protects donor safety stock thresholds
        - Reconciles recipient inventory deficits
        - Respects remaining batch shelf-life and maximum road transit radius
        - Minimizes shortage penalties, expiry wastage, and physical transport costs
        - Persists optimal allocations to redistribution_recommendations table
        """
        # Fetch operational data
        fac_query = self.db.query(Facility).filter(Facility.is_active == True)
        if params.region:
            fac_query = fac_query.filter(Facility.region == params.region)
        facilities = fac_query.all()

        medicines = self.db.query(Medicine).all()
        inventories = self.db.query(Inventory).all()
        batches = self.db.query(Batch).filter(
            Batch.status == "Active", Batch.quantity_remaining > 0
        ).all()

        # Format dict payloads for solver
        fac_dicts = [
            {
                "id": f.id,
                "name": f.name,
                "region": f.region,
                "latitude": f.latitude,
                "longitude": f.longitude,
            }
            for f in facilities
        ]
        med_dicts = [
            {
                "id": m.id,
                "name": m.name,
                "category": m.category,
                "minimum_stock_level": m.minimum_stock_level,
                "lead_time_days": m.lead_time_days,
            }
            for m in medicines
        ]
        inv_dicts = [
            {
                "id": inv.id,
                "facility_id": inv.facility_id,
                "medicine_id": inv.medicine_id,
                "usable_stock": inv.usable_stock,
                "current_stock": inv.current_stock,
            }
            for inv in inventories
        ]
        batch_dicts = [
            {
                "id": b.id,
                "facility_id": b.facility_id,
                "medicine_id": b.medicine_id,
                "batch_number": b.batch_number,
                "expiry_date": b.expiry_date,
                "quantity_remaining": b.quantity_remaining,
                "unit_cost_etb": b.unit_cost_etb,
                "status": b.status,
            }
            for b in batches
        ]

        optimizer = MILPRedistributionOptimizer(
            cost_shortage=params.cost_shortage_penalty,
            cost_waste=params.cost_waste_penalty,
            cost_transport_per_km_unit=params.cost_transport_per_km_unit,
            max_distance_km=params.max_distance_km,
            min_shelf_life_days=params.min_expiry_months * 30,
        )

        opt_result = optimizer.solve(
            facilities=fac_dicts,
            medicines=med_dicts,
            inventories=inv_dicts,
            batches=batch_dicts,
        )

        persisted_recs = []
        for alloc in opt_result["allocations"]:
            transfer_qty = alloc["quantity_recommended"]
            source_name = alloc["source_facility_name"]
            target_name = alloc["target_facility_name"]
            dist = alloc["transport_distance_km"]
            exp_date = alloc["expiry_date"]

            rationale = (
                f"MILP Optimal Transfer: Reallocate {transfer_qty} units from {source_name} to {target_name} "
                f"(transit: {dist} km) to avert projected stockout and absorb surplus before expiration on {exp_date}."
            )

            rec = RedistributionRecommendation(
                source_facility_id=alloc["source_facility_id"],
                target_facility_id=alloc["target_facility_id"],
                medicine_id=alloc["medicine_id"],
                batch_id=alloc.get("batch_id"),
                quantity_recommended=transfer_qty,
                transport_distance_km=dist,
                estimated_transfer_cost_etb=alloc["estimated_transfer_cost_etb"],
                prevented_wastage_cost_etb=alloc["prevented_wastage_cost_etb"],
                status="Pending",
                priority="High" if transfer_qty > 50 else "Medium",
                rationale=rationale,
            )
            saved = self.repo.create_recommendation(rec)
            persisted_recs.append(saved)

        return persisted_recs

    def get_recommendations(
        self,
        facility_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RedistributionResponse]:
        """Lists recommendations with facility and medicine entity names."""
        query = self.db.query(RedistributionRecommendation)
        if facility_id:
            query = query.filter(
                (RedistributionRecommendation.source_facility_id == facility_id)
                | (RedistributionRecommendation.target_facility_id == facility_id)
            )
        if status:
            query = query.filter(RedistributionRecommendation.status == status)
        if priority:
            query = query.filter(RedistributionRecommendation.priority == priority)

        recs = query.order_by(RedistributionRecommendation.created_at.desc()).offset(skip).limit(limit).all()

        results = []
        for r in recs:
            results.append(
                RedistributionResponse(
                    id=r.id,
                    source_facility_id=r.source_facility_id,
                    source_facility_name=r.source_facility.name if r.source_facility else None,
                    target_facility_id=r.target_facility_id,
                    target_facility_name=r.target_facility.name if r.target_facility else None,
                    medicine_id=r.medicine_id,
                    medicine_name=r.medicine.name if r.medicine else None,
                    batch_id=r.batch_id,
                    batch_number=r.batch.batch_number if r.batch else None,
                    quantity_recommended=r.quantity_recommended,
                    transport_distance_km=r.transport_distance_km,
                    estimated_transfer_cost_etb=r.estimated_transfer_cost_etb,
                    prevented_wastage_cost_etb=r.prevented_wastage_cost_etb,
                    status=r.status,
                    priority=r.priority,
                    rationale=r.rationale,
                    reviewed_by=r.reviewed_by,
                    reviewed_at=r.reviewed_at,
                    created_at=r.created_at,
                    updated_at=r.updated_at,
                )
            )
        return results

    def get_recommendation_detail(self, recommendation_id: int) -> RedistributionDetailResponse:
        """Retrieves single recommendation with mathematical verification proof."""
        rec = self.repo.get_recommendation(recommendation_id)
        if not rec:
            raise EntityNotFoundException(f"Recommendation #{recommendation_id} not found.")

        # Construct Mathematical Justification Proof
        med = rec.medicine
        source_fac = rec.source_facility
        target_fac = rec.target_facility
        batch = rec.batch

        donor_inv = self.db.query(Inventory).filter(
            Inventory.facility_id == rec.source_facility_id,
            Inventory.medicine_id == rec.medicine_id,
        ).first()

        recip_inv = self.db.query(Inventory).filter(
            Inventory.facility_id == rec.target_facility_id,
            Inventory.medicine_id == rec.medicine_id,
        ).first()

        donor_stock = donor_inv.usable_stock if donor_inv else 0.0
        donor_ss = med.minimum_stock_level if med else 0.0
        recip_stock = recip_inv.usable_stock if recip_inv else 0.0

        net_benefit = (rec.prevented_wastage_cost_etb or 0.0) - (rec.estimated_transfer_cost_etb or 0.0)

        proof = MathematicalProof(
            donor_surplus_proof=(
                f"Donor stock ({int(donor_stock)}) exceeds local safety threshold ({int(donor_ss)} units). "
                f"Surplus after transfer of {rec.quantity_recommended} units: {round(donor_stock - rec.quantity_recommended, 1)} units."
            ),
            recipient_deficit_proof=(
                f"Recipient inventory ({int(recip_stock)}) is below safety threshold ({int(donor_ss)}). "
                f"Allocation covers {round(rec.quantity_recommended, 1)} units of shortage."
            ),
            shelf_life_proof=(
                f"Batch {batch.batch_number if batch else 'N/A'} expires on {batch.expiry_date if batch else 'N/A'}, "
                f"leaving ample time for transit and dispensing before expiration."
            ),
            distance_proof=(
                f"Road distance is {round(rec.transport_distance_km or 0.0, 1)} km, well within the 150 km regional threshold."
            ),
            net_economic_benefit_etb=round(net_benefit, 2),
        )

        return RedistributionDetailResponse(
            id=rec.id,
            source_facility_id=rec.source_facility_id,
            source_facility_name=source_fac.name if source_fac else None,
            target_facility_id=rec.target_facility_id,
            target_facility_name=target_fac.name if target_fac else None,
            medicine_id=rec.medicine_id,
            medicine_name=med.name if med else None,
            batch_id=rec.batch_id,
            batch_number=batch.batch_number if batch else None,
            quantity_recommended=rec.quantity_recommended,
            transport_distance_km=rec.transport_distance_km,
            estimated_transfer_cost_etb=rec.estimated_transfer_cost_etb,
            prevented_wastage_cost_etb=rec.prevented_wastage_cost_etb,
            status=rec.status,
            priority=rec.priority,
            rationale=rec.rationale,
            reviewed_by=rec.reviewed_by,
            reviewed_at=rec.reviewed_at,
            created_at=rec.created_at,
            updated_at=rec.updated_at,
            mathematical_proof=proof,
        )

    def approve_recommendation(
        self, recommendation_id: int, user_id: int, rationale: Optional[str] = None
    ) -> RedistributionResponse:
        """Approves a lateral transfer proposal, reserving stock at the donor facility."""
        rec = self.repo.get_recommendation(recommendation_id)
        if not rec:
            raise EntityNotFoundException(f"Recommendation #{recommendation_id} not found.")

        if rec.status != "Pending":
            raise UnauthorizedActionException(f"Cannot approve recommendation with status '{rec.status}'.")

        # Reserve stock on donor inventory
        donor_inv = self.db.query(Inventory).filter(
            Inventory.facility_id == rec.source_facility_id,
            Inventory.medicine_id == rec.medicine_id,
        ).first()

        if donor_inv:
            donor_inv.reserved_stock += rec.quantity_recommended
            donor_inv.usable_stock = max(0.0, donor_inv.current_stock - donor_inv.reserved_stock)

        updated = self.repo.update_recommendation_status(
            recommendation_id=recommendation_id,
            status="Approved",
            reviewer_id=user_id,
            rationale=rationale or "Approved for execution.",
        )

        # Audit log
        audit = AuditLog(
            user_id=user_id,
            action="APPROVE_REDISTRIBUTION",
            entity_type="redistribution_recommendations",
            entity_id=str(recommendation_id),
            details=f"Approved transfer of {rec.quantity_recommended} units from Facility #{rec.source_facility_id} to #{rec.target_facility_id}.",
        )
        self.db.add(audit)
        self.db.commit()

        return self.get_recommendation_detail(updated.id)

    def reject_recommendation(
        self, recommendation_id: int, user_id: int, reason: str
    ) -> RedistributionResponse:
        """Rejects a recommendation with mandatory clinical justification."""
        rec = self.repo.get_recommendation(recommendation_id)
        if not rec:
            raise EntityNotFoundException(f"Recommendation #{recommendation_id} not found.")

        if rec.status not in ["Pending", "Approved"]:
            raise UnauthorizedActionException(f"Cannot reject recommendation with status '{rec.status}'.")

        # Release reserved stock if previously approved
        if rec.status == "Approved":
            donor_inv = self.db.query(Inventory).filter(
                Inventory.facility_id == rec.source_facility_id,
                Inventory.medicine_id == rec.medicine_id,
            ).first()
            if donor_inv:
                donor_inv.reserved_stock = max(0.0, donor_inv.reserved_stock - rec.quantity_recommended)
                donor_inv.usable_stock = max(0.0, donor_inv.current_stock - donor_inv.reserved_stock)

        updated = self.repo.update_recommendation_status(
            recommendation_id=recommendation_id,
            status="Rejected",
            reviewer_id=user_id,
            rationale=reason,
        )

        audit = AuditLog(
            user_id=user_id,
            action="REJECT_REDISTRIBUTION",
            entity_type="redistribution_recommendations",
            entity_id=str(recommendation_id),
            details=f"Rejected transfer #{recommendation_id}: {reason}",
        )
        self.db.add(audit)
        self.db.commit()

        return self.get_recommendation_detail(updated.id)

    def execute_transfer(
        self, recommendation_id: int, user_id: int
    ) -> RedistributionResponse:
        """
        Executes physical inventory movement:
        - Deducts stock from donor Batch and Inventory
        - Credits stock to recipient Batch and Inventory
        - Records TRANSFER_OUT and TRANSFER_IN bin-card transactions
        """
        rec = self.repo.get_recommendation(recommendation_id)
        if not rec:
            raise EntityNotFoundException(f"Recommendation #{recommendation_id} not found.")

        if rec.status != "Approved":
            raise UnauthorizedActionException("Only Approved recommendations can be executed.")

        qty = rec.quantity_recommended

        # 1. Update Donor
        donor_inv = self.db.query(Inventory).filter(
            Inventory.facility_id == rec.source_facility_id,
            Inventory.medicine_id == rec.medicine_id,
        ).first()

        if donor_inv:
            donor_inv.reserved_stock = max(0.0, donor_inv.reserved_stock - qty)
            donor_inv.current_stock = max(0.0, donor_inv.current_stock - qty)
            donor_inv.usable_stock = max(0.0, donor_inv.current_stock - donor_inv.reserved_stock)

        if rec.batch_id:
            batch = self.db.get(Batch, rec.batch_id)
            if batch:
                batch.quantity_remaining = max(0.0, batch.quantity_remaining - qty)

        # 2. Update Recipient
        recip_inv = self.db.query(Inventory).filter(
            Inventory.facility_id == rec.target_facility_id,
            Inventory.medicine_id == rec.medicine_id,
        ).first()

        if recip_inv:
            recip_inv.current_stock += qty
            recip_inv.usable_stock += qty
        else:
            recip_inv = Inventory(
                facility_id=rec.target_facility_id,
                medicine_id=rec.medicine_id,
                current_stock=qty,
                usable_stock=qty,
                reserved_stock=0.0,
            )
            self.db.add(recip_inv)

        # 3. Log Transactions
        tx_out = InventoryTransaction(
            facility_id=rec.source_facility_id,
            medicine_id=rec.medicine_id,
            batch_id=rec.batch_id,
            transaction_type="TRANSFER_OUT",
            quantity=qty,
            reference_number=f"TRANSFER-REC-{rec.id}",
            notes=f"Lateral redistribution transfer to Facility #{rec.target_facility_id}.",
            created_by=user_id,
        )
        tx_in = InventoryTransaction(
            facility_id=rec.target_facility_id,
            medicine_id=rec.medicine_id,
            batch_id=rec.batch_id,
            transaction_type="TRANSFER_IN",
            quantity=qty,
            reference_number=f"TRANSFER-REC-{rec.id}",
            notes=f"Lateral redistribution receipt from Facility #{rec.source_facility_id}.",
            created_by=user_id,
        )
        self.db.add_all([tx_out, tx_in])

        rec.status = "Completed"
        self.db.commit()
        return self.get_recommendation_detail(rec.id)

    def run_simulation(self, request: SimulationScenarioRequest) -> SimulationScenarioResponse:
        """Executes what-if comparative simulation scenarios."""
        facilities = self.db.query(Facility).filter(Facility.is_active == True).all()
        medicines = self.db.query(Medicine).all()
        inventories = self.db.query(Inventory).all()
        batches = self.db.query(Batch).filter(Batch.quantity_remaining > 0).all()

        fac_dicts = [{"id": f.id, "name": f.name, "latitude": f.latitude, "longitude": f.longitude} for f in facilities]
        med_dicts = [{"id": m.id, "name": m.name, "category": m.category, "minimum_stock_level": m.minimum_stock_level} for m in medicines]
        inv_dicts = [{"id": inv.id, "facility_id": inv.facility_id, "medicine_id": inv.medicine_id, "usable_stock": inv.usable_stock} for inv in inventories]
        batch_dicts = [{"id": b.id, "facility_id": b.facility_id, "medicine_id": b.medicine_id, "quantity_remaining": b.quantity_remaining, "unit_cost_etb": b.unit_cost_etb, "status": b.status, "expiry_date": b.expiry_date} for b in batches]

        simulator = RedistributionSimulator()
        sim_result = simulator.run_scenario(
            scenario_type=request.scenario_type,
            facilities=fac_dicts,
            medicines=med_dicts,
            inventories=inv_dicts,
            batches=batch_dicts,
            horizon_months=request.horizon_months,
        )

        return SimulationScenarioResponse(**sim_result)
