import math
from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.facility import Facility
from app.models.batch import Batch
from app.models.medicine import Medicine
from app.models.inventory import Inventory
from app.models.recommendation import RedistributionRecommendation
from app.repositories.prediction_repository import PredictionRepository
from app.schemas.recommendation import RedistributionOptimizationRun


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points in kilometers."""
    r = 6371.0  # Earth's radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


class RedistributionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PredictionRepository(db)

    def optimize_and_generate_recommendations(
        self, params: RedistributionOptimizationRun
    ) -> List[RedistributionRecommendation]:
        """
        Constrained redistribution matching heuristic:
        1. Find source candidate facilities that have surplus or expiry risk.
        2. Find target candidate facilities facing stockouts.
        3. Constrain by max_distance_km and minimum remaining shelf-life.
        4. Prioritize high prevented wastage value vs transport cost.
        """
        facilities_query = self.db.query(Facility).filter(Facility.is_active == True)
        if params.region:
            facilities_query = facilities_query.filter(Facility.region == params.region)
        facilities = facilities_query.all()

        today = date.today()
        recommendations: List[RedistributionRecommendation] = []

        # Find deficit and surplus pairs
        for med in self.db.query(Medicine).all():
            deficit_facilities = []
            surplus_batches = []

            for fac in facilities:
                inv = self.db.query(Inventory).filter(
                    Inventory.facility_id == fac.id,
                    Inventory.medicine_id == med.id
                ).first()

                if not inv or inv.usable_stock < med.minimum_stock_level:
                    needed_qty = med.minimum_stock_level - (inv.usable_stock if inv else 0.0)
                    if needed_qty > 0:
                        deficit_facilities.append((fac, needed_qty))

                # Check batches for surplus
                batches = self.db.query(Batch).filter(
                    Batch.facility_id == fac.id,
                    Batch.medicine_id == med.id,
                    Batch.status == "Active",
                    Batch.quantity_remaining > 20
                ).all()

                for b in batches:
                    months_left = (b.expiry_date - today).days / 30.0
                    if months_left >= params.min_expiry_months:
                        surplus_batches.append((fac, b))

            # Match deficit with surplus
            for target_fac, needed_qty in deficit_facilities:
                if needed_qty <= 0:
                    continue

                for source_fac, batch in surplus_batches:
                    if source_fac.id == target_fac.id or batch.quantity_remaining <= 0:
                        continue

                    # Distance check
                    dist = 45.0  # default fallback km
                    if source_fac.latitude and source_fac.longitude and target_fac.latitude and target_fac.longitude:
                        dist = haversine_distance_km(
                            source_fac.latitude, source_fac.longitude,
                            target_fac.latitude, target_fac.longitude
                        )

                    if dist > params.max_distance_km:
                        continue

                    transfer_qty = min(needed_qty, batch.quantity_remaining * 0.5)
                    if transfer_qty < 5:
                        continue

                    transport_cost = round(dist * 12.5, 2)  # ~12.5 ETB per km transport cost
                    prevented_wastage = round(transfer_qty * batch.unit_cost_etb, 2)

                    rec = RedistributionRecommendation(
                        source_facility_id=source_fac.id,
                        target_facility_id=target_fac.id,
                        medicine_id=med.id,
                        batch_id=batch.id,
                        quantity_recommended=round(transfer_qty, 1),
                        transport_distance_km=round(dist, 1),
                        estimated_transfer_cost_etb=transport_cost,
                        prevented_wastage_cost_etb=prevented_wastage,
                        status="Pending",
                        priority="High" if transfer_qty > 50 else "Medium",
                        rationale=(
                            f"Redistribute {round(transfer_qty, 1)} units from {source_fac.name} to {target_fac.name} "
                            f"(distance: {round(dist, 1)} km) to alleviate shortage before batch expiry on {batch.expiry_date}."
                        ),
                    )
                    saved = self.repo.create_recommendation(rec)
                    recommendations.append(saved)
                    needed_qty -= transfer_qty
                    batch.quantity_remaining -= transfer_qty

        return recommendations
