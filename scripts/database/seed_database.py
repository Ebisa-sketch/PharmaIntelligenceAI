"""
PharmaIntelligence AI - Database Seeding Script

Populates the database with foundational roles, initial administrator user,
authentic Ethiopian healthcare facilities, and national essential medicines.
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import date, datetime, timedelta, timezone

# Ensure backend root is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.database.connection import SessionLocal
from app.core.security import get_password_hash
from app.models import (
    Role,
    User,
    Facility,
    Medicine,
    Inventory,
    Batch,
    InventoryTransaction,
    AuditLog,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("db_seed")

ROLES_DATA = [
    {"name": "admin", "description": "System Administrator with full management access"},
    {"name": "pharmacy_manager", "description": "Facility Pharmacy Manager for facility inventory & batch management"},
    {"name": "regional_manager", "description": "Regional Supply Chain Manager for cross-facility oversight & redistribution"},
    {"name": "data_analyst", "description": "Data Analyst / Researcher for data quality and AI experiments"},
    {"name": "auditor", "description": "Auditor with read-only compliance access to audit logs and actions"},
]

ETHIOPIAN_FACILITIES = [
    {
        "code": "ETH-ADD-TASH",
        "name": "Tikur Anbessa (Black Lion) Specialized Hospital",
        "facility_type": "Specialized Referral Hospital",
        "region": "Addis Ababa",
        "zone": "Addis Ababa",
        "woreda": "Lideta",
        "latitude": 9.0142,
        "longitude": 38.7525,
        "storage_capacity_m3": 1200.0,
        "is_active": True,
    },
    {
        "code": "ETH-ADD-SPHMMC",
        "name": "St. Paul's Hospital Millennium Medical College",
        "facility_type": "Specialized Hospital",
        "region": "Addis Ababa",
        "zone": "Addis Ababa",
        "woreda": "Gulele",
        "latitude": 9.0558,
        "longitude": 38.7303,
        "storage_capacity_m3": 950.0,
        "is_active": True,
    },
    {
        "code": "ETH-ORO-JIMMA",
        "name": "Jimma University Medical Center (JUMC)",
        "facility_type": "Specialized Referral Hospital",
        "region": "Oromia",
        "zone": "Jimma Zone",
        "woreda": "Jimma Town",
        "latitude": 7.6763,
        "longitude": 36.8344,
        "storage_capacity_m3": 850.0,
        "is_active": True,
    },
    {
        "code": "ETH-SID-HAWASSA",
        "name": "Hawassa University Comprehensive Specialized Hospital",
        "facility_type": "Comprehensive Specialized Hospital",
        "region": "Sidama",
        "zone": "Hawassa City",
        "woreda": "Menehariya",
        "latitude": 7.0504,
        "longitude": 38.4955,
        "storage_capacity_m3": 750.0,
        "is_active": True,
    },
    {
        "code": "ETH-AMH-FELEGE",
        "name": "Felege Hiwot Comprehensive Specialized Hospital",
        "facility_type": "Comprehensive Specialized Hospital",
        "region": "Amhara",
        "zone": "West Gojjam",
        "woreda": "Bahir Dar",
        "latitude": 11.5936,
        "longitude": 37.3908,
        "storage_capacity_m3": 700.0,
        "is_active": True,
    },
    {
        "code": "ETH-AMH-GONDAR",
        "name": "University of Gondar Comprehensive Specialized Hospital",
        "facility_type": "Specialized Referral Hospital",
        "region": "Amhara",
        "zone": "Central Gondar",
        "woreda": "Gondar Town",
        "latitude": 12.6083,
        "longitude": 37.4528,
        "storage_capacity_m3": 800.0,
        "is_active": True,
    },
]

ETHIOPIAN_ESSENTIAL_MEDICINES = [
    {
        "code": "MED-AMX-500",
        "name": "Amoxicillin 500mg Capsule",
        "brand_name": "Amoxil",
        "category": "Anti-infectives / Antibiotics",
        "dosage_form": "Capsule",
        "strength": "500mg",
        "unit_of_measure": "100 Capsules/Pack",
        "is_essential": True,
        "vital_classification": "Vital",
        "minimum_stock_level": 500.0,
        "reorder_point": 1200.0,
        "lead_time_days": 25,
    },
    {
        "code": "MED-ALU-20120",
        "name": "Artemether + Lumefantrine 20/120mg Tablet",
        "brand_name": "Coartem",
        "category": "Antimalarials",
        "dosage_form": "Tablet",
        "strength": "20mg/120mg",
        "unit_of_measure": "24 Tablets/Blister",
        "is_essential": True,
        "vital_classification": "Vital",
        "minimum_stock_level": 800.0,
        "reorder_point": 2000.0,
        "lead_time_days": 20,
    },
    {
        "code": "MED-PAR-500",
        "name": "Paracetamol 500mg Tablet",
        "brand_name": "Panadol",
        "category": "Analgesics & Antipyretics",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "unit_of_measure": "1000 Tablets/Jar",
        "is_essential": True,
        "vital_classification": "Essential",
        "minimum_stock_level": 1000.0,
        "reorder_point": 2500.0,
        "lead_time_days": 15,
    },
    {
        "code": "MED-CTX-1G",
        "name": "Ceftriaxone Sodium 1g Powder for Injection",
        "brand_name": "Rocephin",
        "category": "Anti-infectives / Cephalosporins",
        "dosage_form": "Vial / Powder for Injection",
        "strength": "1g",
        "unit_of_measure": "10 Vials/Box",
        "is_essential": True,
        "vital_classification": "Vital",
        "minimum_stock_level": 300.0,
        "reorder_point": 700.0,
        "lead_time_days": 30,
    },
    {
        "code": "MED-MET-500",
        "name": "Metformin Hydrochloride 500mg Tablet",
        "brand_name": "Glucophage",
        "category": "Antidiabetics",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "unit_of_measure": "100 Tablets/Pack",
        "is_essential": True,
        "vital_classification": "Vital",
        "minimum_stock_level": 600.0,
        "reorder_point": 1500.0,
        "lead_time_days": 28,
    },
    {
        "code": "MED-OXY-10IU",
        "name": "Oxytocin 10 IU/ml Injection",
        "brand_name": "Pitocin",
        "category": "Obstetric & Maternal Health",
        "dosage_form": "Ampoule",
        "strength": "10 IU/ml",
        "unit_of_measure": "10 Ampoules/Box",
        "is_essential": True,
        "vital_classification": "Vital",
        "minimum_stock_level": 200.0,
        "reorder_point": 500.0,
        "lead_time_days": 18,
    },
    {
        "code": "MED-ORS-20G",
        "name": "Oral Rehydration Salts (ORS) Sachet (Low Osmolarity)",
        "brand_name": "Oral Rehydration Salts",
        "category": "Gastrointestinal",
        "dosage_form": "Powder for Oral Solution",
        "strength": "20.5g/L",
        "unit_of_measure": "100 Sachets/Box",
        "is_essential": True,
        "vital_classification": "Essential",
        "minimum_stock_level": 1200.0,
        "reorder_point": 3000.0,
        "lead_time_days": 14,
    },
    {
        "code": "MED-AML-5MG",
        "name": "Amlodipine Besylate 5mg Tablet",
        "brand_name": "Norvasc",
        "category": "Cardiovascular / Antihypertensive",
        "dosage_form": "Tablet",
        "strength": "5mg",
        "unit_of_measure": "30 Tablets/Pack",
        "is_essential": True,
        "vital_classification": "Essential",
        "minimum_stock_level": 400.0,
        "reorder_point": 1000.0,
        "lead_time_days": 21,
    },
]


def seed_database() -> None:
    session = SessionLocal()
    try:
        logger.info("Starting database seeding...")

        # 1. Roles
        roles_by_name = {}
        for r_data in ROLES_DATA:
            role = session.query(Role).filter_by(name=r_data["name"]).first()
            if not role:
                role = Role(name=r_data["name"], description=r_data["description"])
                session.add(role)
                session.flush()
                logger.info("Created role: %s", role.name)
            roles_by_name[role.name] = role

        # 2. Facilities
        facilities_by_code = {}
        for f_data in ETHIOPIAN_FACILITIES:
            facility = session.query(Facility).filter_by(code=f_data["code"]).first()
            if not facility:
                facility = Facility(**f_data)
                session.add(facility)
                session.flush()
                logger.info("Created facility: %s (%s)", facility.name, facility.code)
            facilities_by_code[facility.code] = facility

        # 3. Users
        admin_user = session.query(User).filter_by(email="admin@pharmaintelligence.et").first()
        if not admin_user:
            admin_user = User(
                email="admin@pharmaintelligence.et",
                full_name="National System Administrator",
                hashed_password=get_password_hash("Admin123!Secure"),
                is_active=True,
                role_id=roles_by_name["admin"].id,
                facility_id=facilities_by_code["ETH-ADD-TASH"].id,
            )
            session.add(admin_user)
            logger.info("Created default system administrator: admin@pharmaintelligence.et")

        pharmacy_mgr = session.query(User).filter_by(email="manager.tash@pharmaintelligence.et").first()
        if not pharmacy_mgr:
            pharmacy_mgr = User(
                email="manager.tash@pharmaintelligence.et",
                full_name="TASH Pharmacy Operations Lead",
                hashed_password=get_password_hash("Manager123!Secure"),
                is_active=True,
                role_id=roles_by_name["pharmacy_manager"].id,
                facility_id=facilities_by_code["ETH-ADD-TASH"].id,
            )
            session.add(pharmacy_mgr)
            logger.info("Created facility pharmacy manager: manager.tash@pharmaintelligence.et")

        session.flush()

        # 4. Medicines
        medicines_by_code = {}
        for m_data in ETHIOPIAN_ESSENTIAL_MEDICINES:
            med = session.query(Medicine).filter_by(code=m_data["code"]).first()
            if not med:
                med = Medicine(**m_data)
                session.add(med)
                session.flush()
                logger.info("Created medicine: %s (%s)", med.name, med.code)
            medicines_by_code[med.code] = med

        # 5. Inventories & Batches for sample facilities
        today = date.today()
        sample_batches = [
            ("ETH-ADD-TASH", "MED-AMX-500", "BATCH-AMX-2026A", today + timedelta(days=240), 1500.0, 1200.0, 4.50),
            ("ETH-ADD-TASH", "MED-AMX-500", "BATCH-AMX-2026B", today + timedelta(days=60), 800.0, 250.0, 4.50),  # Near expiry
            ("ETH-ADD-TASH", "MED-ALU-20120", "BATCH-COA-2026X", today + timedelta(days=365), 2400.0, 2100.0, 12.00),
            ("ETH-ADD-TASH", "MED-CTX-1G", "BATCH-CTX-2026Q", today + timedelta(days=180), 500.0, 420.0, 28.50),
            ("ETH-SID-HAWASSA", "MED-AMX-500", "BATCH-AMX-HW01", today + timedelta(days=300), 1000.0, 850.0, 4.50),
            ("ETH-SID-HAWASSA", "MED-ALU-20120", "BATCH-COA-HW02", today + timedelta(days=400), 1500.0, 1300.0, 12.00),
            ("ETH-ORO-JIMMA", "MED-AMX-500", "BATCH-AMX-JM01", today + timedelta(days=120), 600.0, 110.0, 4.50),  # Low stock
            ("ETH-ORO-JIMMA", "MED-PAR-500", "BATCH-PAR-JM01", today + timedelta(days=500), 3000.0, 2800.0, 2.20),
        ]

        for fac_code, med_code, b_num, exp_date, init_qty, cur_qty, unit_cost in sample_batches:
            fac = facilities_by_code[fac_code]
            med = medicines_by_code[med_code]
            batch = session.query(Batch).filter_by(facility_id=fac.id, medicine_id=med.id, batch_number=b_num).first()
            if not batch:
                batch = Batch(
                    facility_id=fac.id,
                    medicine_id=med.id,
                    batch_number=b_num,
                    expiry_date=exp_date,
                    manufacturing_date=exp_date - timedelta(days=730),
                    quantity_initial=init_qty,
                    quantity_remaining=cur_qty,
                    unit_cost_etb=unit_cost,
                    status="Active",
                )
                session.add(batch)
                session.flush()

                # Add initial receipt transaction
                tx = InventoryTransaction(
                    facility_id=fac.id,
                    medicine_id=med.id,
                    batch_id=batch.id,
                    transaction_type="Receipt",
                    quantity=init_qty,
                    reference_number=f"PO-{b_num}",
                    transaction_date=datetime.now(timezone.utc) - timedelta(days=60),
                    notes="Opening balance / initial procurement consignment",
                    created_by=admin_user.id,
                )
                session.add(tx)

        # 6. Aggregated facility inventories
        for fac_code, fac in facilities_by_code.items():
            for med_code, med in medicines_by_code.items():
                inv = session.query(Inventory).filter_by(facility_id=fac.id, medicine_id=med.id).first()
                if not inv:
                    batches = session.query(Batch).filter_by(facility_id=fac.id, medicine_id=med.id).all()
                    stock_qty = sum(b.quantity_remaining for b in batches)
                    status_label = "Adequate"
                    if stock_qty == 0:
                        status_label = "Stockout"
                    elif stock_qty < med.minimum_stock_level:
                        status_label = "Understocked"
                    elif stock_qty > (med.reorder_point * 1.5):
                        status_label = "Overstocked"

                    inv = Inventory(
                        facility_id=fac.id,
                        medicine_id=med.id,
                        current_stock=stock_qty,
                        reserved_stock=0.0,
                        usable_stock=stock_qty,
                        average_monthly_consumption=max(100.0, stock_qty / 3.0),
                        months_of_stock=round(stock_qty / max(1.0, (stock_qty / 3.0)), 1),
                        stock_status=status_label,
                        last_counted_date=datetime.now(timezone.utc),
                    )
                    session.add(inv)

        # 7. Audit log for seeding event
        audit = AuditLog(
            user_id=admin_user.id,
            action="DATABASE_SEED",
            entity_type="System",
            entity_id="ALL",
            details="Seeded initial system roles, facilities, essential medicines, and baseline inventory balances.",
            ip_address="127.0.0.1",
        )
        session.add(audit)

        session.commit()
        logger.info("[✓] Database seeding successfully completed!")
    except Exception as exc:
        session.rollback()
        logger.error("[✗] Error during database seeding: %s", exc, exc_info=True)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
