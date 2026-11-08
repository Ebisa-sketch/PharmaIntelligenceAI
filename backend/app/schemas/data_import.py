from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class DataQualityIssueSummary(BaseModel):
    id: Optional[int] = None
    row_number: Optional[int] = None
    issue_type: str
    severity: str
    field_name: Optional[str] = None
    description: str
    is_resolved: bool = False

    model_config = ConfigDict(from_attributes=True)


class DataImportResponse(BaseModel):
    id: int
    facility_id: int
    facility_name: Optional[str] = None
    filename: str
    file_hash_sha256: str
    total_rows: int
    valid_rows: int
    rejected_rows: int
    dq_score: float
    status: str
    created_at: datetime
    quality_issues_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class DataImportDetailResponse(DataImportResponse):
    quality_issues: List[DataQualityIssueSummary] = []


class IngestionPreviewResult(BaseModel):
    filename: str
    total_rows: int
    estimated_valid_rows: int
    estimated_rejected_rows: int
    preliminary_dq_score: float
    detected_headers: List[str]
    sample_rows: List[dict]
    preview_issues: List[dict]

