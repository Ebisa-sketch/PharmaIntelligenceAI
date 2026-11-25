from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    facilities,
    medicines,
    inventory,
    batches,
    imports,
    data_quality,
    forecasting,
    stockout,
    expiry,
    redistribution,
    experiments,
    reports,
    audit_logs,
    notifications,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(facilities.router, prefix="/facilities", tags=["Facilities"])
api_router.include_router(medicines.router, prefix="/medicines", tags=["Medicines"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(batches.router, prefix="/batches", tags=["Batches"])
api_router.include_router(imports.router, prefix="/imports", tags=["Data Imports"])
api_router.include_router(data_quality.router, prefix="/data-quality", tags=["Data Quality Intelligence"])
api_router.include_router(forecasting.router, prefix="/forecasting", tags=["Demand Forecasting"])
api_router.include_router(stockout.router, prefix="/stockout", tags=["Stockout Risk Intelligence"])
api_router.include_router(expiry.router, prefix="/expiry", tags=["Expiry Risk Intelligence"])
api_router.include_router(redistribution.router, prefix="/redistribution", tags=["Redistribution Engine"])
api_router.include_router(experiments.router, prefix="/experiments", tags=["Research & Experiments"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports & Analytics"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["Audit & Governance"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
