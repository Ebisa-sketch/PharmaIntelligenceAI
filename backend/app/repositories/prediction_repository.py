from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.prediction import Prediction
from app.models.forecast import Forecast
from app.models.recommendation import RedistributionRecommendation


class PredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_predictions(
        self,
        facility_id: Optional[int] = None,
        medicine_id: Optional[int] = None,
        risk_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Prediction]:
        stmt = select(Prediction)
        if facility_id:
            stmt = stmt.where(Prediction.facility_id == facility_id)
        if medicine_id:
            stmt = stmt.where(Prediction.medicine_id == medicine_id)
        if risk_type:
            stmt = stmt.where(Prediction.risk_type == risk_type)
        stmt = stmt.order_by(Prediction.prediction_date.desc()).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def save_prediction(self, prediction: Prediction) -> Prediction:
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def get_latest_forecast(self, facility_id: int, medicine_id: int) -> Optional[Forecast]:
        stmt = select(Forecast).where(
            Forecast.facility_id == facility_id,
            Forecast.medicine_id == medicine_id
        ).order_by(Forecast.forecast_date.desc())
        return self.db.scalars(stmt).first()

    def save_forecast(self, forecast: Forecast) -> Forecast:
        self.db.add(forecast)
        self.db.commit()
        self.db.refresh(forecast)
        return forecast

    def get_recommendations(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[RedistributionRecommendation]:
        stmt = select(RedistributionRecommendation)
        if status:
            stmt = stmt.where(RedistributionRecommendation.status == status)
        if priority:
            stmt = stmt.where(RedistributionRecommendation.priority == priority)
        stmt = stmt.order_by(RedistributionRecommendation.created_at.desc()).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_recommendation(self, recommendation_id: int) -> Optional[RedistributionRecommendation]:
        return self.db.get(RedistributionRecommendation, recommendation_id)

    def create_recommendation(self, rec: RedistributionRecommendation) -> RedistributionRecommendation:
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec

    def update_recommendation_status(
        self,
        recommendation_id: int,
        status: str,
        reviewer_id: int,
        rationale: Optional[str] = None,
    ) -> Optional[RedistributionRecommendation]:
        rec = self.get_recommendation(recommendation_id)
        if not rec:
            return None
        rec.status = status
        rec.reviewed_by = reviewer_id
        rec.reviewed_at = datetime.now(timezone.utc)
        if rationale:
            rec.rationale = f"{rec.rationale} | Review: {rationale}"
        self.db.commit()
        self.db.refresh(rec)
        return rec
