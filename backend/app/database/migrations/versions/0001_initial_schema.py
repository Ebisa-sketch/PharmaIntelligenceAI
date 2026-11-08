"""0001_initial_schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-11-08 21:25:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. roles
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_roles_id", "roles", ["id"])
    op.create_index("ix_roles_name", "roles", ["name"], unique=True)

    # 2. facilities
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("facility_type", sa.String(length=100), nullable=False),
        sa.Column("region", sa.String(length=100), nullable=False),
        sa.Column("zone", sa.String(length=100), nullable=True),
        sa.Column("woreda", sa.String(length=100), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("storage_capacity_m3", sa.Float(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.CheckConstraint("storage_capacity_m3 IS NULL OR storage_capacity_m3 >= 0", name="ck_facility_storage_capacity"),
    )
    op.create_index("ix_facilities_id", "facilities", ["id"])
    op.create_index("ix_facilities_code", "facilities", ["code"], unique=True)
    op.create_index("ix_facilities_name", "facilities", ["name"])
    op.create_index("ix_facilities_region_type", "facilities", ["region", "facility_type"])

    # 3. users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_users_facility_id", "users", ["facility_id"])

    # 4. medicines
    op.create_table(
        "medicines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("brand_name", sa.String(length=255), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("dosage_form", sa.String(length=100), nullable=False),
        sa.Column("strength", sa.String(length=100), nullable=False),
        sa.Column("unit_of_measure", sa.String(length=50), nullable=False),
        sa.Column("is_essential", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("vital_classification", sa.String(length=20), nullable=False, server_default=sa.text("'Essential'")),
        sa.Column("minimum_stock_level", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("reorder_point", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("lead_time_days", sa.Integer(), nullable=False, server_default=sa.text("30")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.CheckConstraint("minimum_stock_level >= 0", name="ck_medicine_min_stock_non_negative"),
        sa.CheckConstraint("reorder_point >= 0", name="ck_medicine_reorder_point_non_negative"),
        sa.CheckConstraint("lead_time_days >= 0", name="ck_medicine_lead_time_non_negative"),
    )
    op.create_index("ix_medicines_id", "medicines", ["id"])
    op.create_index("ix_medicines_code", "medicines", ["code"], unique=True)
    op.create_index("ix_medicines_name", "medicines", ["name"])
    op.create_index("ix_medicines_category_vital", "medicines", ["category", "vital_classification"])

    # 5. inventories
    op.create_table(
        "inventories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("medicine_id", sa.Integer(), nullable=False),
        sa.Column("current_stock", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("reserved_stock", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("usable_stock", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("average_monthly_consumption", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("months_of_stock", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("stock_status", sa.String(length=50), nullable=False, server_default=sa.text("'Adequate'")),
        sa.Column("last_counted_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("facility_id", "medicine_id", name="uq_facility_medicine_inventory"),
        sa.CheckConstraint("current_stock >= 0", name="ck_inventory_current_stock_non_negative"),
        sa.CheckConstraint("usable_stock >= 0", name="ck_inventory_usable_stock_non_negative"),
    )
    op.create_index("ix_inventories_id", "inventories", ["id"])
    op.create_index("ix_inventories_facility_status", "inventories", ["facility_id", "stock_status"])
    op.create_index("ix_inventories_medicine", "inventories", ["medicine_id"])

    # 6. batches
    op.create_table(
        "batches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("medicine_id", sa.Integer(), nullable=False),
        sa.Column("batch_number", sa.String(length=100), nullable=False),
        sa.Column("expiry_date", sa.Date(), nullable=False),
        sa.Column("manufacturing_date", sa.Date(), nullable=True),
        sa.Column("quantity_initial", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("quantity_remaining", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("unit_cost_etb", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("status", sa.String(length=50), nullable=False, server_default=sa.text("'Active'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("facility_id", "medicine_id", "batch_number", name="uq_facility_medicine_batch"),
        sa.CheckConstraint("quantity_initial >= 0", name="ck_batch_quantity_initial_non_negative"),
        sa.CheckConstraint("quantity_remaining >= 0", name="ck_batch_quantity_remaining_non_negative"),
        sa.CheckConstraint("unit_cost_etb >= 0", name="ck_batch_unit_cost_non_negative"),
    )
    op.create_index("ix_batches_id", "batches", ["id"])
    op.create_index("ix_batches_facility_expiry", "batches", ["facility_id", "expiry_date"])
    op.create_index("ix_batches_medicine_expiry", "batches", ["medicine_id", "expiry_date"])
    op.create_index("ix_batches_status_expiry", "batches", ["status", "expiry_date"])

    # 7. data_imports
    op.create_table(
        "data_imports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("uploaded_by_user_id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("file_hash_sha256", sa.String(length=64), nullable=False),
        sa.Column("total_rows", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("valid_rows", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("rejected_rows", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("dq_score", sa.Float(), nullable=False, server_default=sa.text("100.0")),
        sa.Column("status", sa.String(length=50), nullable=False, server_default=sa.text("'COMPLETED'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"]),
        sa.ForeignKeyConstraint(["uploaded_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_imports_id", "data_imports", ["id"])
    op.create_index("ix_data_imports_facility_id", "data_imports", ["facility_id"])
    op.create_index("ix_data_imports_hash", "data_imports", ["file_hash_sha256"])

    # 8. data_quality_issues
    op.create_table(
        "data_quality_issues",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("import_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("medicine_id", sa.Integer(), nullable=True),
        sa.Column("issue_type", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("field_name", sa.String(length=100), nullable=True),
        sa.Column("row_number", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("is_resolved", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["import_id"], ["data_imports.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"]),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_quality_issues_id", "data_quality_issues", ["id"])
    op.create_index("ix_data_quality_issues_facility_sev", "data_quality_issues", ["facility_id", "severity"])
    op.create_index("ix_data_quality_issues_type", "data_quality_issues", ["issue_type"])

    # 9. inventory_transactions
    op.create_table(
        "inventory_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("medicine_id", sa.Integer(), nullable=False),
        sa.Column("batch_id", sa.Integer(), nullable=True),
        sa.Column("import_id", sa.Integer(), nullable=True),
        sa.Column("transaction_type", sa.String(length=50), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("reference_number", sa.String(length=100), nullable=True),
        sa.Column("transaction_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"]),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"]),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"]),
        sa.ForeignKeyConstraint(["import_id"], ["data_imports.id"]),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tx_id", "inventory_transactions", ["id"])
    op.create_index("ix_tx_facility_date", "inventory_transactions", ["facility_id", "transaction_date"])
    op.create_index("ix_tx_facility_medicine_date", "inventory_transactions", ["facility_id", "medicine_id", "transaction_date"])
    op.create_index("ix_tx_batch", "inventory_transactions", ["batch_id"])

    # 10. forecasts
    op.create_table(
        "forecasts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("medicine_id", sa.Integer(), nullable=False),
        sa.Column("model_type", sa.String(length=100), nullable=False),
        sa.Column("forecast_date", sa.Date(), nullable=False),
        sa.Column("target_period_start", sa.Date(), nullable=False),
        sa.Column("target_period_end", sa.Date(), nullable=False),
        sa.Column("forecast_value", sa.Float(), nullable=False),
        sa.Column("confidence_interval_lower", sa.Float(), nullable=False),
        sa.Column("confidence_interval_upper", sa.Float(), nullable=False),
        sa.Column("mape_score", sa.Float(), nullable=True),
        sa.Column("uncertainty_score", sa.Float(), nullable=True),
        sa.Column("features_used", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("forecast_value >= 0", name="ck_forecast_value_non_negative"),
    )
    op.create_index("ix_forecasts_id", "forecasts", ["id"])
    op.create_index("ix_forecast_facility_medicine_period", "forecasts", ["facility_id", "medicine_id", "target_period_start"])
    op.create_index("ix_forecast_model_date", "forecasts", ["model_type", "forecast_date"])

    # 11. predictions
    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("medicine_id", sa.Integer(), nullable=False),
        sa.Column("batch_id", sa.Integer(), nullable=True),
        sa.Column("risk_type", sa.String(length=50), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.String(length=50), nullable=False),
        sa.Column("estimated_stockout_date", sa.Date(), nullable=True),
        sa.Column("estimated_expired_units", sa.Float(), nullable=True),
        sa.Column("estimated_financial_loss_etb", sa.Float(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("prediction_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("risk_score >= 0.0 AND risk_score <= 1.0", name="ck_prediction_risk_score_range"),
    )
    op.create_index("ix_predictions_id", "predictions", ["id"])
    op.create_index("ix_pred_facility_risk", "predictions", ["facility_id", "risk_type", "risk_level"])
    op.create_index("ix_pred_medicine_risk", "predictions", ["medicine_id", "risk_type"])
    op.create_index("ix_pred_date", "predictions", ["prediction_date"])

    # 12. redistribution_recommendations
    op.create_table(
        "redistribution_recommendations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_facility_id", sa.Integer(), nullable=False),
        sa.Column("target_facility_id", sa.Integer(), nullable=False),
        sa.Column("medicine_id", sa.Integer(), nullable=False),
        sa.Column("batch_id", sa.Integer(), nullable=True),
        sa.Column("quantity_recommended", sa.Float(), nullable=False),
        sa.Column("transport_distance_km", sa.Float(), nullable=True),
        sa.Column("estimated_transfer_cost_etb", sa.Float(), nullable=True),
        sa.Column("prevented_wastage_cost_etb", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default=sa.text("'Pending'")),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default=sa.text("'Medium'")),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("reviewed_by", sa.Integer(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_facility_id"], ["facilities.id"]),
        sa.ForeignKeyConstraint(["target_facility_id"], ["facilities.id"]),
        sa.ForeignKeyConstraint(["medicine_id"], ["medicines.id"]),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"]),
        sa.ForeignKeyConstraint(["reviewed_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("quantity_recommended > 0", name="ck_rec_quantity_positive"),
        sa.CheckConstraint("source_facility_id != target_facility_id", name="ck_rec_distinct_facilities"),
    )
    op.create_index("ix_redistribution_id", "redistribution_recommendations", ["id"])
    op.create_index("ix_rec_facilities_status", "redistribution_recommendations", ["source_facility_id", "target_facility_id", "status"])
    op.create_index("ix_rec_status_priority", "redistribution_recommendations", ["status", "priority"])

    # 13. audit_logs
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(length=50), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_logs_id", "audit_logs", ["id"])
    op.create_index("ix_audit_logs_user_timestamp", "audit_logs", ["user_id", "timestamp"])
    op.create_index("ix_audit_logs_entity", "audit_logs", ["entity_type", "entity_id"])
    op.create_index("ix_audit_logs_action_timestamp", "audit_logs", ["action", "timestamp"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("redistribution_recommendations")
    op.drop_table("predictions")
    op.drop_table("forecasts")
    op.drop_table("inventory_transactions")
    op.drop_table("data_quality_issues")
    op.drop_table("data_imports")
    op.drop_table("batches")
    op.drop_table("inventories")
    op.drop_table("medicines")
    op.drop_table("users")
    op.drop_table("facilities")
    op.drop_table("roles")

