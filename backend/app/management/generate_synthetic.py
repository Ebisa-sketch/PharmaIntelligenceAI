"""
Management command to generate and optionally seed synthetic pharmaceutical data.

Usage:
  python -m app.management.generate_synthetic --months 36 --facilities 8 --anomaly-rate 0.03 --seed-db
  python -m app.management.generate_synthetic --export-csv --output-dir data/synthetic/sample_data
"""

import argparse
import json
import os
import sys

# Ensure the backend and root packages are importable
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from data.synthetic.generators.synthetic_generator import SyntheticDataGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic pharmaceutical inventory data for PharmaIntelligence AI"
    )
    parser.add_argument("--months", type=int, default=36, help="Number of historical months (default: 36)")
    parser.add_argument("--facilities", type=int, default=8, help="Number of facilities (max 8, default: 8)")
    parser.add_argument("--anomaly-rate", type=float, default=0.03, help="Anomaly injection rate (0.0 - 0.10, default: 0.03)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--export-csv", action="store_true", help="Export batch and transaction CSVs per facility")
    parser.add_argument("--export-json", action="store_true", help="Export full dataset as JSON")
    parser.add_argument("--output-dir", type=str, default="data/synthetic/sample_data", help="Output directory for exports")
    parser.add_argument("--seed-db", action="store_true", help="Seed the generated data into the database")
    parser.add_argument("--summary", action="store_true", default=True, help="Print dataset summary (default: true)")

    args = parser.parse_args()

    print(f"🧬 PharmaIntelligence AI — Synthetic Data Generator")
    print(f"   Facilities: {args.facilities}")
    print(f"   Months: {args.months}")
    print(f"   Anomaly Rate: {args.anomaly_rate:.1%}")
    print(f"   Random Seed: {args.seed}")
    print()

    generator = SyntheticDataGenerator(
        num_facilities=args.facilities,
        num_months=args.months,
        anomaly_rate=args.anomaly_rate,
        seed=args.seed,
    )

    print("⏳ Generating dataset...")
    dataset = generator.generate_full_dataset()
    metadata = dataset["metadata"]

    print(f"✅ Dataset generated successfully!")
    print(f"   Facilities:    {metadata['num_facilities']}")
    print(f"   Medicines:     {metadata['num_medicines']}")
    print(f"   Batches:       {metadata['num_batches']}")
    print(f"   Transactions:  {metadata['num_transactions']}")
    print(f"   Inventories:   {metadata['num_inventory_records']}")
    print(f"   Anomalies:     {metadata['anomalies_count']}")
    print()

    # ─── Export CSV ───
    if args.export_csv:
        os.makedirs(args.output_dir, exist_ok=True)

        for facility in generator.facilities:
            fac_code = facility["code"]
            safe_code = fac_code.replace("-", "_")

            # Batches CSV
            fac_batches = generator.get_facility_batches(dataset, fac_code)
            csv_content = generator.export_batches_csv(fac_batches)
            csv_path = os.path.join(args.output_dir, f"batches_{safe_code}.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                f.write(csv_content)

            # Transactions CSV
            fac_txs = generator.get_facility_transactions(dataset, fac_code)
            csv_content = generator.export_transactions_csv(fac_txs)
            csv_path = os.path.join(args.output_dir, f"transactions_{safe_code}.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                f.write(csv_content)

            print(f"   📄 Exported: {safe_code} ({len(fac_batches)} batches, {len(fac_txs)} transactions)")

        # Anomaly manifest
        anomaly_path = os.path.join(args.output_dir, "anomaly_manifest.json")
        with open(anomaly_path, "w", encoding="utf-8") as f:
            json.dump(dataset["anomalies_injected"], f, indent=2, default=str)
        print(f"   📄 Anomaly manifest: {anomaly_path}")
        print()

    # ─── Export JSON ───
    if args.export_json:
        os.makedirs(args.output_dir, exist_ok=True)
        json_path = os.path.join(args.output_dir, "full_dataset.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2, default=str)
        print(f"   📦 Full dataset JSON: {json_path}")
        print()

    # ─── Seed Database ───
    if args.seed_db:
        print("🌱 Seeding database with synthetic data...")
        try:
            from app.database.connection import SessionLocal
            from app.database.base import Base
            from app.database.connection import engine
            from app.models import Facility, Medicine, Batch, Inventory, InventoryTransaction

            Base.metadata.create_all(bind=engine)
            db = SessionLocal()

            try:
                # Check if data already exists
                existing_facilities = db.query(Facility).count()
                if existing_facilities > 0:
                    print(f"   ⚠️  Database already has {existing_facilities} facilities. Skipping seed to prevent duplicates.")
                    print("   💡 Truncate tables first if you want to re-seed.")
                else:
                    # Seed facilities
                    for fac_data in dataset["facilities"]:
                        fac = Facility(**fac_data)
                        db.add(fac)
                    db.flush()

                    # Seed medicines
                    for med_data in dataset["medicines"]:
                        med = Medicine(**med_data)
                        db.add(med)
                    db.flush()

                    # Build lookup maps
                    fac_map = {f.code: f.id for f in db.query(Facility).all()}
                    med_map = {m.code: m.id for m in db.query(Medicine).all()}

                    # Seed batches
                    batch_map = {}
                    for b_data in dataset["batches"]:
                        fac_id = fac_map.get(b_data["facility_code"])
                        med_id = med_map.get(b_data["medicine_code"])
                        if fac_id and med_id and b_data["batch_number"]:
                            batch = Batch(
                                facility_id=fac_id,
                                medicine_id=med_id,
                                batch_number=b_data["batch_number"],
                                expiry_date=b_data["expiry_date"],
                                manufacturing_date=b_data.get("manufacturing_date"),
                                quantity_initial=b_data["quantity_initial"],
                                quantity_remaining=max(0, b_data["quantity_remaining"]),
                                unit_cost_etb=b_data.get("unit_cost_etb", 0.0),
                                status=b_data["status"],
                            )
                            db.add(batch)
                    db.flush()

                    # Build batch lookup
                    for batch_obj in db.query(Batch).all():
                        key = (batch_obj.facility_id, batch_obj.medicine_id, batch_obj.batch_number)
                        batch_map[key] = batch_obj.id

                    # Seed inventories
                    for inv_data in dataset["inventories"]:
                        fac_id = fac_map.get(inv_data["facility_code"])
                        med_id = med_map.get(inv_data["medicine_code"])
                        if fac_id and med_id:
                            inv = Inventory(
                                facility_id=fac_id,
                                medicine_id=med_id,
                                current_stock=max(0, inv_data["current_stock"]),
                                usable_stock=max(0, inv_data.get("usable_stock", inv_data["current_stock"])),
                                average_monthly_consumption=inv_data.get("average_monthly_consumption", 0.0),
                                months_of_stock=inv_data.get("months_of_stock", 0.0),
                                stock_status=inv_data.get("stock_status", "Adequate"),
                            )
                            db.add(inv)
                    db.flush()

                    # Seed transactions (sample — limit to keep DB manageable)
                    tx_count = 0
                    for tx_data in dataset["transactions"]:
                        fac_id = fac_map.get(tx_data["facility_code"])
                        med_id = med_map.get(tx_data["medicine_code"])
                        if fac_id and med_id:
                            batch_id = None
                            if tx_data.get("batch_number"):
                                batch_id = batch_map.get((fac_id, med_id, tx_data["batch_number"]))

                            tx = InventoryTransaction(
                                facility_id=fac_id,
                                medicine_id=med_id,
                                batch_id=batch_id,
                                transaction_type=tx_data["transaction_type"],
                                quantity=tx_data["quantity"],
                                transaction_date=tx_data["transaction_date"],
                                reference_number=tx_data.get("reference_number"),
                                notes=tx_data.get("notes"),
                            )
                            db.add(tx)
                            tx_count += 1

                    db.commit()
                    print(f"   ✅ Seeded {len(dataset['facilities'])} facilities, {len(dataset['medicines'])} medicines,")
                    print(f"      {len(dataset['batches'])} batches, {len(dataset['inventories'])} inventories, {tx_count} transactions.")

            finally:
                db.close()

        except ImportError as e:
            print(f"   ❌ Cannot seed DB: {e}")
            print("   💡 Run from the backend directory with virtual environment activated.")

    # ─── Summary Statistics ───
    if args.summary:
        print("─" * 55)
        print("📊 Dataset Summary")
        print("─" * 55)

        # Demand category breakdown
        categories = {}
        for tx in dataset["transactions"]:
            cat = tx["transaction_type"]
            categories[cat] = categories.get(cat, 0) + 1

        for cat, count in sorted(categories.items()):
            print(f"   {cat:<25} {count:>8} transactions")

        print()

        # Anomaly breakdown
        if dataset["anomalies_injected"]:
            anomaly_counts = {}
            for a in dataset["anomalies_injected"]:
                t = a["type"]
                anomaly_counts[t] = anomaly_counts.get(t, 0) + 1
            print("🔬 Injected Anomalies (Ground Truth for DQI Benchmarking):")
            for atype, count in sorted(anomaly_counts.items()):
                print(f"   {atype:<30} {count:>5} occurrences")

    print()
    print("Done. ✨")


if __name__ == "__main__":
    main()

