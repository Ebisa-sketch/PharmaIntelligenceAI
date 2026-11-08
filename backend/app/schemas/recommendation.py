from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class RedistributionRequest(BaseModel):
    source_facility_id: int
    target_facility_id: int
    medicine_id: int
    batch_id: Optional[int] = None
    quantity_recommended: float
    priority: str = "Medium"
    rationale: str


class RedistributionStatusUpdate(BaseModel):
    status: str  # Approved, Rejected, In_Transit, Completed
    rationale: Optional[str] = None


class RedistributionOptimizationRun(BaseModel):
    region: Optional[str] = None
    max_distance_km: float = 150.0
    min_expiry_months: int = 3
    priority_level: Optional[str] = None
    cost_shortage_penalty: float = 100.0
    cost_waste_penalty: float = 50.0
    cost_transport_per_km_unit: float = 0.02


class RedistributionResponse(BaseModel):
    id: int
    source_facility_id: int
    source_facility_name: Optional[str] = None
    target_facility_id: int
    target_facility_name: Optional[str] = None
    medicine_id: int
    medicine_name: Optional[str] = None
    batch_id: Optional[int] = None
    batch_number: Optional[str] = None
    quantity_recommended: float
    transport_distance_km: Optional[float] = None
    estimated_transfer_cost_etb: Optional[float] = None
    prevented_wastage_cost_etb: Optional[float] = None
    status: str
    priority: str
    rationale: str
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MathematicalProof(BaseModel):
    donor_surplus_proof: str
    recipient_deficit_proof: str
    shelf_life_proof: str
    distance_proof: str
    net_economic_benefit_etb: float


class RedistributionDetailResponse(RedistributionResponse):
    mathematical_proof: Optional[MathematicalProof] = None


class ScenarioKPI(BaseModel):
    total_shortages_unmet: float
    total_expired_units: float
    total_expired_loss_etb: float
    total_transferred_units: float
    total_transport_cost_etb: float
    net_economic_benefit_etb: float
    service_level_percent: float


class SimulationScenarioRequest(BaseModel):
    scenario_type: str = "collaborative_network"  # baseline_isolated, collaborative_network, local_cluster, epidemic_spike
    horizon_months: int = 6
    max_distance_km: float = 150.0


class SimulationScenarioResponse(BaseModel):
    scenario_type: str
    scenario_name: str
    description: str
    facilities_evaluated: int
    medicines_evaluated: int
    baseline_kpis: ScenarioKPI
    scenario_kpis: ScenarioKPI
    improvement_summary: Dict[str, Any]
