"""
PharmaIntelligence AI - Database Seeding Script

Loads initial seed data or generated synthetic datasets into database tables.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

FACILITY_SEEDS = [
    {"facility_id": "FAC-NYC01", "name": "Manhattan General Hospital Pharmacy", "facility_type": "Hospital", "city": "New York", "region": "NY", "latitude": 40.7128, "longitude": -74.0060},
    {"facility_id": "FAC-BOS01", "name": "Boston Central Distribution Depot", "facility_type": "Warehouse", "city": "Boston", "region": "MA", "latitude": 42.3601, "longitude": -71.0589},
    {"facility_id": "FAC-CHI01", "name": "Chicago Lakeshore Health Center", "facility_type": "Hospital", "city": "Chicago", "region": "IL", "latitude": 41.8781, "longitude": -87.6298},
    {"facility_id": "FAC-LAX01", "name": "West Coast Clinical Supply Hub", "facility_type": "Warehouse", "city": "Los Angeles", "region": "CA", "latitude": 34.0522, "longitude": -118.2437},
    {"facility_id": "FAC-HOU01", "name": "Houston Medical Regional Pharmacy", "facility_type": "Retail", "city": "Houston", "region": "TX", "latitude": 29.7604, "longitude": -95.3698},
]


def seed(database_url: str, data_dir: Path):
    try:
        from sqlalchemy import create_engine, text
        import pandas as pd
    except ImportError:
        print("[!] SQLAlchemy and pandas are required for seed_database.py.", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Connecting to database: {database_url}")
    engine = create_engine(database_url)

    # 1. Seed Facilities
    print("[*] Seeding facilities...")
    df_fac = pd.DataFrame(FACILITY_SEEDS)
    df_fac.to_sql("facilities", engine, if_exists="append", index=False)
    print(f"[✓] Seeded {len(df_fac)} facilities.")

    # 2. Check for synthetic datasets
    med_csv = data_dir / "synthetic_medicines.csv"
    inv_csv = data_dir / "synthetic_inventory.csv"
    bat_csv = data_dir / "synthetic_batches.csv"

    if med_csv.exists():
        print(f"[*] Seeding medicines from {med_csv}...")
        df_med = pd.read_csv(med_csv)
        df_med.to_sql("medicines", engine, if_exists="append", index=False)
        print(f"[✓] Seeded {len(df_med)} medicines.")

    if inv_csv.exists():
        print(f"[*] Seeding inventory from {inv_csv}...")
        df_inv = pd.read_csv(inv_csv)
        df_inv.to_sql("inventory", engine, if_exists="append", index=False)
        print(f"[✓] Seeded {len(df_inv)} inventory records.")

    if bat_csv.exists():
        print(f"[*] Seeding batches from {bat_csv}...")
        df_bat = pd.read_csv(bat_csv)
        df_bat.to_sql("batches", engine, if_exists="append", index=False)
        print(f"[✓] Seeded {len(df_bat)} batches.")

    print("[✓] Database seeding completed successfully.")


def main():
    parser = argparse.ArgumentParser(description="Seed PharmaIntelligence AI database")
    parser.add_argument("--db-url", default=os.getenv("DATABASE_URL", "sqlite:///./pharmaintelligence.db"))
    parser.add_argument("--data-dir", type=Path, default=Path("data/synthetic/sample_data"))
    args = parser.parse_args()

    seed(args.db_url, args.data_dir)


if __name__ == "__main__":
    main()
