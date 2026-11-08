"""
PharmaIntelligence AI - Synthetic Pharmaceutical Data Generator

Generates realistic mock datasets for medicines, multi-facility inventory records,
and batch tracking with expiry dynamics.
"""

from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pandas as pd

SAMPLE_MEDICINES = [
    {"id": "MED-AMOXI500", "name": "Amoxicillin 500mg Capsule", "generic": "Amoxicillin", "atc": "J01CA04", "form": "Capsule", "strength": "500mg", "unit": "mg", "class": "Antibacterial", "storage": "Room Temperature"},
    {"id": "MED-AZITH250", "name": "Azithromycin 250mg Tablet", "generic": "Azithromycin", "atc": "J01FA10", "form": "Tablet", "strength": "250mg", "unit": "mg", "class": "Macrolide", "storage": "Room Temperature"},
    {"id": "MED-INSUL100", "name": "Human Insulin 100 IU/ml Vial", "generic": "Insulin Human", "atc": "A10AB01", "form": "Injection", "strength": "100 IU/ml", "unit": "IU", "class": "Antidiabetic", "storage": "Refrigerated (2-8C)"},
    {"id": "MED-PARAC500", "name": "Paracetamol 500mg Tablet", "generic": "Paracetamol", "atc": "N02BE01", "form": "Tablet", "strength": "500mg", "unit": "mg", "class": "Analgesic", "storage": "Room Temperature"},
    {"id": "MED-METFO850", "name": "Metformin HCl 850mg Tablet", "generic": "Metformin", "atc": "A10BA02", "form": "Tablet", "strength": "850mg", "unit": "mg", "class": "Antidiabetic", "storage": "Room Temperature"},
    {"id": "MED-ATORV020", "name": "Atorvastatin 20mg Tablet", "generic": "Atorvastatin", "atc": "C10AA05", "form": "Tablet", "strength": "20mg", "unit": "mg", "class": "Lipid Modifying", "storage": "Room Temperature"},
    {"id": "MED-SALBU100", "name": "Salbutamol 100mcg Inhaler", "generic": "Salbutamol", "atc": "R03AC02", "form": "Inhaler", "strength": "100mcg", "unit": "mcg", "class": "Antiasthmatic", "storage": "Room Temperature"},
    {"id": "MED-CEFTR001", "name": "Ceftriaxone 1g Powder for Injection", "generic": "Ceftriaxone", "atc": "J01DD04", "form": "Injection", "strength": "1g", "unit": "g", "class": "Cephalosporin", "storage": "Controlled Room Temperature"},
]

SAMPLE_FACILITIES = [
    "FAC-NYC01", "FAC-BOS01", "FAC-CHI01", "FAC-LAX01", "FAC-HOU01"
]


def generate_data(output_dir: Path, num_records: int = 50):
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)

    # 1. Medicines
    med_df = pd.DataFrame([
        {
            "medicine_id": m["id"],
            "name": m["name"],
            "generic_name": m["generic"],
            "brand_name": m["name"].split()[0],
            "atc_code": m["atc"],
            "dosage_form": m["form"],
            "strength": m["strength"],
            "unit_of_measure": m["unit"],
            "therapeutic_class": m["class"],
            "is_prescription_required": True,
            "storage_condition": m["storage"],
            "standard_pack_size": random.choice([10, 20, 30, 50, 100]),
        }
        for m in SAMPLE_MEDICINES
    ])
    med_path = output_dir / "synthetic_medicines.csv"
    med_df.to_csv(med_path, index=False)
    print(f"[✓] Generated {len(med_df)} medicines -> {med_path}")

    # 2. Inventory Records
    inventory_records = []
    inv_id = 1000
    for fac in SAMPLE_FACILITIES:
        for med in SAMPLE_MEDICINES:
            soh = random.randint(10, 2000)
            reorder = random.randint(100, 500)
            safety = int(reorder * 0.4)
            inventory_records.append({
                "inventory_id": f"INV-{inv_id}",
                "facility_id": fac,
                "medicine_id": med["id"],
                "stock_on_hand": soh,
                "stock_reserved": random.randint(0, min(soh, 50)),
                "stock_in_transit": random.choice([0, 100, 250]),
                "reorder_level": reorder,
                "reorder_quantity": random.randint(300, 1000),
                "safety_stock": safety,
                "unit_cost": round(random.uniform(2.5, 85.0), 2),
                "selling_price": round(random.uniform(5.0, 120.0), 2),
                "average_daily_consumption": round(random.uniform(5.0, 45.0), 2),
                "lead_time_days": random.randint(2, 14),
                "last_updated_at": now.isoformat(),
            })
            inv_id += 1

    inv_df = pd.DataFrame(inventory_records)
    inv_path = output_dir / "synthetic_inventory.csv"
    inv_df.to_csv(inv_path, index=False)
    print(f"[✓] Generated {len(inv_df)} inventory records -> {inv_path}")

    # 3. Batches
    batches = []
    bat_id = 5000
    for inv in inventory_records[:num_records]:
        mfg_offset = random.randint(90, 700)
        exp_offset = random.randint(30, 365)
        mfg_date = (now - timedelta(days=mfg_offset)).date()
        exp_date = (now + timedelta(days=exp_offset)).date()
        init_qty = random.randint(200, 2000)

        batches.append({
            "batch_id": f"BAT-{bat_id}",
            "batch_number": f"LOT-{random.randint(100000, 999999)}",
            "medicine_id": inv["medicine_id"],
            "facility_id": inv["facility_id"],
            "supplier_id": f"SUP-{random.randint(1, 10):02d}",
            "manufacturing_date": mfg_date.isoformat(),
            "expiration_date": exp_date.isoformat(),
            "initial_quantity": init_qty,
            "remaining_quantity": random.randint(0, init_qty),
            "unit_purchase_cost": inv["unit_cost"],
            "status": "Near Expiry" if exp_offset < 60 else "Active",
            "storage_location": f"Aisle-{random.randint(1, 12)}-Shelf-{random.randint(1, 6)}"
        })
        bat_id += 1

    bat_df = pd.DataFrame(batches)
    bat_path = output_dir / "synthetic_batches.csv"
    bat_df.to_csv(bat_path, index=False)
    print(f"[✓] Generated {len(bat_df)} batches -> {bat_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic pharmaceutical dataset")
    parser.add_argument("--output-dir", type=Path, default=Path("data/synthetic/sample_data"))
    parser.add_argument("--count", type=int, default=50, help="Number of batch samples to generate")
    args = parser.parse_args()

    generate_data(args.output_dir, args.count)


if __name__ == "__main__":
    main()
