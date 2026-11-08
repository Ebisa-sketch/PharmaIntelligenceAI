from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class DimensionScore(BaseModel):
    dimension: str
    score: float
    status: str
    issue_count: int
    description: str


class DataQualityAssessmentResponse(BaseModel):
    facility_id: int
    facility_name: Optional[str] = None
    dqi_score: float
    status: str  # Excellent (>=90), Good (>=75), Degraded (>=60), Critical (<60)
    dimensions: List[DimensionScore]
    total_issues: int
    critical_issues_count: int
    warning_issues_count: int
    total_batches_analyzed: int
    total_inventories_analyzed: int
    assessed_at: datetime


class DataQualityIssueFilter(BaseModel):
    facility_id: Optional[int] = None
    import_id: Optional[int] = None
    severity: Optional[str] = None
    issue_type: Optional[str] = None
    is_resolved: Optional[bool] = None


class DataQualityIssueItem(BaseModel):
    id: int
    import_id: int
    facility_id: int
    facility_name: Optional[str] = None
    medicine_id: Optional[int] = None
    medicine_name: Optional[str] = None
    issue_type: str
    severity: str
    field_name: Optional[str] = None
    row_number: Optional[int] = None
    description: str
    details: Optional[str] = None
    is_resolved: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IssueResolutionRequest(BaseModel):
    resolved: bool = True
    resolution_notes: Optional[str] = None

