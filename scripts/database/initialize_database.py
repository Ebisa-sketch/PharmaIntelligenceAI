"""
PharmaIntelligence AI - Database Initialization Script

Creates all core tables, indices, and extensions for PostgreSQL / SQLite databases.
"""

from __future__ import annotations

import argparse
import os
import sys

SCHEMA_SQL = """
-- Extensions (for PostgreSQL)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Facilities
CREATE TABLE IF NOT EXISTS facilities (
    facility_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    facility_type VARCHAR(50) NOT NULL, -- Hospital, Retail, Warehouse, Clinic
    address VARCHAR(255),
    city VARCHAR(100),
    region VARCHAR(100),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Medicines Catalog
CREATE TABLE IF NOT EXISTS medicines (
    medicine_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    generic_name VARCHAR(255) NOT NULL,
    brand_name VARCHAR(255),
    atc_code VARCHAR(10) NOT NULL,
    ndc_code VARCHAR(32),
    dosage_form VARCHAR(50) NOT NULL,
    strength VARCHAR(50) NOT NULL,
    unit_of_measure VARCHAR(20) NOT NULL,
    therapeutic_class VARCHAR(100) NOT NULL,
    is_prescription_required BOOLEAN DEFAULT TRUE,
    storage_condition VARCHAR(100),
    standard_pack_size INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Inventory Status
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id VARCHAR(32) PRIMARY KEY,
    facility_id VARCHAR(32) NOT NULL REFERENCES facilities(facility_id) ON DELETE CASCADE,
    medicine_id VARCHAR(32) NOT NULL REFERENCES medicines(medicine_id) ON DELETE CASCADE,
    stock_on_hand INTEGER NOT NULL DEFAULT 0,
    stock_reserved INTEGER NOT NULL DEFAULT 0,
    stock_in_transit INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 0,
    reorder_quantity INTEGER NOT NULL DEFAULT 100,
    safety_stock INTEGER NOT NULL DEFAULT 0,
    unit_cost NUMERIC(10, 2),
    selling_price NUMERIC(10, 2),
    average_daily_consumption NUMERIC(8, 2) DEFAULT 0.0,
    lead_time_days INTEGER DEFAULT 7,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_facility_medicine UNIQUE (facility_id, medicine_id)
);

-- 4. Batches & Expiry Tracking
CREATE TABLE IF NOT EXISTS batches (
    batch_id VARCHAR(32) PRIMARY KEY,
    batch_number VARCHAR(64) NOT NULL,
    medicine_id VARCHAR(32) NOT NULL REFERENCES medicines(medicine_id) ON DELETE CASCADE,
    facility_id VARCHAR(32) NOT NULL REFERENCES facilities(facility_id) ON DELETE CASCADE,
    supplier_id VARCHAR(32),
    manufacturing_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    initial_quantity INTEGER NOT NULL,
    remaining_quantity INTEGER NOT NULL,
    unit_purchase_cost NUMERIC(10, 2),
    status VARCHAR(32) DEFAULT 'Active',
    storage_location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Demand & Dispensing History
CREATE TABLE IF NOT EXISTS dispensing_events (
    event_id VARCHAR(32) PRIMARY KEY,
    facility_id VARCHAR(32) NOT NULL REFERENCES facilities(facility_id),
    medicine_id VARCHAR(32) NOT NULL REFERENCES medicines(medicine_id),
    batch_id VARCHAR(32) REFERENCES batches(batch_id),
    quantity_dispensed INTEGER NOT NULL,
    dispensed_at TIMESTAMP NOT NULL,
    patient_category VARCHAR(50),
    stockout_prevented BOOLEAN DEFAULT FALSE
);

-- Indices for rapid query performance
CREATE INDEX IF NOT EXISTS idx_inv_medicine ON inventory(medicine_id);
CREATE INDEX IF NOT EXISTS idx_inv_facility ON inventory(facility_id);
CREATE INDEX IF NOT EXISTS idx_batches_expiry ON batches(expiration_date, status);
CREATE INDEX IF NOT EXISTS idx_dispensing_time ON dispensing_events(medicine_id, facility_id, dispensed_at);
"""


def initialize_db(database_url: str):
    print(f"[*] Initializing database connection: {database_url}")
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(database_url)
        with engine.connect() as conn:
            for statement in SCHEMA_SQL.split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))
            conn.commit()
        print("[✓] All database schemas and indices created successfully.")
    except ImportError:
        print("[!] SQLAlchemy is required to run initialize_database.py directly.", file=sys.stderr)
        print("[*] Outputting SQL schema script for manual execution:")
        print(SCHEMA_SQL)


def main():
    parser = argparse.ArgumentParser(description="Initialize PharmaIntelligence AI database tables")
    parser.add_argument("--db-url", default=os.getenv("DATABASE_URL", "sqlite:///./pharmaintelligence.db"),
                        help="Database connection URL (PostgreSQL or SQLite)")
    args = parser.parse_args()
    initialize_db(args.db_url)


if __name__ == "__main__":
    main()
