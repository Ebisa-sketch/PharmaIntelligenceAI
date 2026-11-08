"""
Synthetic Pharmaceutical Dataset Generator for PharmaIntelligence AI

Generates realistic Ethiopian healthcare facility inventory data with:
- Compound Poisson-Gamma demand distributions per medicine category
- Sinusoidal seasonal multipliers (rainy season malaria/respiratory peaks)
- Stockout censoring simulation (zero recorded when inventory exhausted)
- Log-normal lead-time modeling for EPSS delivery delays
- FEFO-prioritized batch drawdowns with realistic shelf-life ranges
- Controlled anomaly injection for benchmarking the DQI engine

Reference: docs/05-data-documentation/dataset-specification.md §4
"""

import csv
import io
import math
import random
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# ──────────────────────────────────────────────────────────────
# Ethiopian Healthcare Facility Templates
# ──────────────────────────────────────────────────────────────

FACILITY_TEMPLATES = [
    {
        "code": "ETH-AA-TASH-01",
        "name": "Tikur Anbessa Specialized Hospital",
        "facility_type": "Specialized Referral Hospital",
        "region": "Addis Ababa",
        "zone": "Lideta",
        "woreda": "Woreda 07",
        "latitude": 9.0054,
        "longitude": 38.7468,
        "catchment_population": 5_000_000,
        "demand_multiplier": 2.5,
    },
    {
        "code": "ETH-AA-SPH-02",
        "name": "St. Paul's Hospital Millennium Medical College",
        "facility_type": "Specialized Referral Hospital",
        "region": "Addis Ababa",
        "zone": "Gulele",
        "woreda": "Woreda 01",
        "latitude": 9.0400,
        "longitude": 38.7300,
        "catchment_population": 3_500_000,
        "demand_multiplier": 2.0,
    },
    {
        "code": "ETH-OR-JUMC-03",
        "name": "Jimma University Medical Center",
        "facility_type": "Specialized Referral Hospital",
        "region": "Oromia",
        "zone": "Jimma",
        "woreda": "Jimma Town",
        "latitude": 7.6740,
        "longitude": 36.8300,
        "catchment_population": 2_000_000,
        "demand_multiplier": 1.8,
    },
    {
        "code": "ETH-SD-HURH-04",
        "name": "Hawassa University Referral Hospital",
        "facility_type": "General Hospital",
        "region": "Sidama",
        "zone": "Hawassa",
        "woreda": "Hawassa Town",
        "latitude": 7.0504,
        "longitude": 38.4955,
        "catchment_population": 1_200_000,
        "demand_multiplier": 1.4,
    },
    {
        "code": "ETH-AM-UOGH-05",
        "name": "University of Gondar Hospital",
        "facility_type": "Specialized Referral Hospital",
        "region": "Amhara",
        "zone": "North Gondar",
        "woreda": "Gondar Town",
        "latitude": 12.6000,
        "longitude": 37.4667,
        "catchment_population": 1_500_000,
        "demand_multiplier": 1.6,
    },
    {
        "code": "ETH-AA-ZEWDITU-06",
        "name": "Zewditu Memorial Hospital",
        "facility_type": "General Hospital",
        "region": "Addis Ababa",
        "zone": "Kirkos",
        "woreda": "Woreda 04",
        "latitude": 9.0100,
        "longitude": 38.7500,
        "catchment_population": 800_000,
        "demand_multiplier": 1.2,
    },
    {
        "code": "ETH-OR-ADAMA-07",
        "name": "Adama General Hospital",
        "facility_type": "General Hospital",
        "region": "Oromia",
        "zone": "East Shewa",
        "woreda": "Adama Town",
        "latitude": 8.5400,
        "longitude": 39.2700,
        "catchment_population": 600_000,
        "demand_multiplier": 1.0,
    },
    {
        "code": "ETH-TG-AYDER-08",
        "name": "Ayder Comprehensive Specialized Hospital",
        "facility_type": "Specialized Referral Hospital",
        "region": "Tigray",
        "zone": "Mekelle",
        "woreda": "Mekelle Town",
        "latitude": 13.4960,
        "longitude": 39.4753,
        "catchment_population": 1_800_000,
        "demand_multiplier": 1.5,
    },
]

# ──────────────────────────────────────────────────────────────
# Essential Medicines Catalogue (NEML representative basket)
# ──────────────────────────────────────────────────────────────

MEDICINE_TEMPLATES = [
    # High-volume fast-movers (Smooth demand)
    {
        "code": "MED-AMOX-500",
        "name": "Amoxicillin 500mg Capsule",
        "category": "Antibiotics",
        "dosage_form": "Capsule",
        "strength": "500mg",
        "unit_of_measure": "Capsule",
        "vital_classification": "Essential",
        "demand_category": "smooth",
        "base_monthly_demand": 2400,
        "demand_cv": 0.15,
        "shelf_life_months": (24, 36),
        "unit_cost_etb": 2.50,
    },
    {
        "code": "MED-PARA-500",
        "name": "Paracetamol 500mg Tablet",
        "category": "Analgesics",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "unit_of_measure": "Tablet",
        "vital_classification": "Essential",
        "demand_category": "smooth",
        "base_monthly_demand": 5000,
        "demand_cv": 0.12,
        "shelf_life_months": (24, 36),
        "unit_cost_etb": 0.80,
    },
    {
        "code": "MED-METR-250",
        "name": "Metronidazole 250mg Tablet",
        "category": "Antibiotics",
        "dosage_form": "Tablet",
        "strength": "250mg",
        "unit_of_measure": "Tablet",
        "vital_classification": "Essential",
        "demand_category": "smooth",
        "base_monthly_demand": 1800,
        "demand_cv": 0.18,
        "shelf_life_months": (24, 36),
        "unit_cost_etb": 1.20,
    },
    # Intermittent / Critical Life-Saving
    {
        "code": "MED-OXYT-10",
        "name": "Oxytocin 10 IU/ml Injection",
        "category": "Reproductive Health",
        "dosage_form": "Injection",
        "strength": "10 IU/ml",
        "unit_of_measure": "Ampoule",
        "vital_classification": "Vital",
        "demand_category": "intermittent",
        "base_monthly_demand": 120,
        "demand_cv": 0.55,
        "shelf_life_months": (12, 24),
        "unit_cost_etb": 25.00,
    },
    {
        "code": "MED-MGSO4-50",
        "name": "Magnesium Sulfate 50% Injection",
        "category": "Emergency Medicine",
        "dosage_form": "Injection",
        "strength": "50%",
        "unit_of_measure": "Ampoule",
        "vital_classification": "Vital",
        "demand_category": "intermittent",
        "base_monthly_demand": 60,
        "demand_cv": 0.65,
        "shelf_life_months": (18, 36),
        "unit_cost_etb": 35.00,
    },
    # Chronic Disease Maintenance (Smooth to Erratic)
    {
        "code": "MED-METF-500",
        "name": "Metformin 500mg Tablet",
        "category": "Endocrinology",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "unit_of_measure": "Tablet",
        "vital_classification": "Essential",
        "demand_category": "erratic",
        "base_monthly_demand": 900,
        "demand_cv": 0.30,
        "shelf_life_months": (24, 36),
        "unit_cost_etb": 1.50,
    },
    {
        "code": "MED-ENAL-5",
        "name": "Enalapril 5mg Tablet",
        "category": "Cardiovascular",
        "dosage_form": "Tablet",
        "strength": "5mg",
        "unit_of_measure": "Tablet",
        "vital_classification": "Essential",
        "demand_category": "erratic",
        "base_monthly_demand": 1200,
        "demand_cv": 0.25,
        "shelf_life_months": (24, 36),
        "unit_cost_etb": 1.80,
    },
    # Seasonal Morbidity Commodities (Seasonal/Lumpy)
    {
        "code": "MED-ARLU-20",
        "name": "Artemether-Lumefantrine (Coartem) 20/120mg",
        "category": "Antimalarials",
        "dosage_form": "Tablet",
        "strength": "20/120mg",
        "unit_of_measure": "Tablet",
        "vital_classification": "Vital",
        "demand_category": "seasonal",
        "base_monthly_demand": 800,
        "demand_cv": 0.45,
        "shelf_life_months": (18, 30),
        "unit_cost_etb": 12.00,
    },
    {
        "code": "MED-ORS-SAL",
        "name": "ORS (Oral Rehydration Salts) Sachet",
        "category": "Gastrointestinal",
        "dosage_form": "Powder",
        "strength": "Standard",
        "unit_of_measure": "Sachet",
        "vital_classification": "Essential",
        "demand_category": "seasonal",
        "base_monthly_demand": 1500,
        "demand_cv": 0.35,
        "shelf_life_months": (24, 36),
        "unit_cost_etb": 3.00,
    },
    {
        "code": "MED-COTX-480",
        "name": "Cotrimoxazole 480mg Tablet",
        "category": "Antibiotics",
        "dosage_form": "Tablet",
        "strength": "480mg",
        "unit_of_measure": "Tablet",
        "vital_classification": "Essential",
        "demand_category": "smooth",
        "base_monthly_demand": 2000,
        "demand_cv": 0.20,
        "shelf_life_months": (24, 36),
        "unit_cost_etb": 1.10,
    },
]

# ──────────────────────────────────────────────────────────────
# Anomaly injection types for DQI benchmarking
# ──────────────────────────────────────────────────────────────

ANOMALY_TYPES = [
    "negative_stock",          # Negative quantity_remaining in batch
    "missing_batch_number",    # Empty batch number
    "expired_active",          # Batch past expiry but status=Active
    "duplicate_batch",         # Same facility+medicine+batch duplicated
    "reconciliation_mismatch", # Inventory stock != sum of batch quantities
    "future_transaction_date", # Transaction date in the future
    "missing_medicine_code",   # Transaction references nonexistent medicine
    "quantity_overflow",       # Remaining > initial
]


class SyntheticDataGenerator:
    """
    Generates synthetic pharmaceutical inventory data for Ethiopian healthcare
    facilities, designed to model realistic demand patterns, supply chain
    delays, seasonal variations, and controlled data quality anomalies.
    """

    def __init__(
        self,
        num_facilities: int = 8,
        num_months: int = 36,
        anomaly_rate: float = 0.03,
        seed: int = 42,
    ):
        """
        Args:
            num_facilities: Number of facilities to simulate (max 8 templates)
            num_months: Historical months to generate (minimum 12)
            anomaly_rate: Fraction of records injected with intentional anomalies (0.0 - 0.10)
            seed: Random seed for reproducibility
        """
        self.num_facilities = min(num_facilities, len(FACILITY_TEMPLATES))
        self.num_months = max(12, num_months)
        self.anomaly_rate = max(0.0, min(0.10, anomaly_rate))
        self.rng = np.random.default_rng(seed)
        random.seed(seed)

        self.facilities = FACILITY_TEMPLATES[: self.num_facilities]
        self.medicines = MEDICINE_TEMPLATES
        self.anomalies_injected: List[Dict[str, Any]] = []

    def _seasonal_multiplier(self, month: int, category: str) -> float:
        """
        Ethiopian seasonal demand multiplier.
        - Kiremt (June-Sep): Peak malaria & respiratory (antimalarials, antibiotics)
        - Bega (Oct-Jan): Dry season, lower demand
        - Belg (Feb-May): Short rainy season, moderate demand
        """
        # Month 1=Jan ... 12=Dec
        phase = 2 * math.pi * (month - 1) / 12.0

        if category == "seasonal":
            # Artemether/ORS: Strong peak in Jun-Sep (Ethiopian rainy season)
            return 1.0 + 0.6 * math.sin(phase - math.pi / 6)
        elif category == "smooth":
            # Mild seasonal variation
            return 1.0 + 0.10 * math.sin(phase)
        elif category == "intermittent":
            # Low baseline, random spikes
            return 1.0 + 0.15 * math.sin(phase + math.pi / 4)
        elif category == "erratic":
            # Moderate variance, slight seasonality
            return 1.0 + 0.20 * math.sin(phase - math.pi / 3)
        return 1.0

    def _generate_demand(
        self,
        base_demand: float,
        cv: float,
        demand_multiplier: float,
        category: str,
        month: int,
    ) -> int:
        """
        Generates non-negative integer demand using compound Poisson-Gamma model.
        Negative Binomial is used as the marginal distribution.
        """
        seasonal = self._seasonal_multiplier(month, category)
        mean_demand = base_demand * demand_multiplier * seasonal

        if mean_demand <= 0:
            return 0

        # Negative Binomial parameterization
        variance = (mean_demand * cv) ** 2 + mean_demand
        p = mean_demand / variance if variance > mean_demand else 0.999
        n = mean_demand * p / (1 - p) if p < 1.0 else mean_demand

        n = max(1.0, n)
        p = max(0.001, min(0.999, p))

        demand = int(self.rng.negative_binomial(n, p))
        return max(0, demand)

    def _generate_lead_time_days(self) -> int:
        """Log-normal EPSS delivery delays (µ=21 days, σ=10 days)."""
        mu_ln = math.log(21 ** 2 / math.sqrt(21 ** 2 + 10 ** 2))
        sigma_ln = math.sqrt(math.log(1 + (10 / 21) ** 2))
        lead_time = int(self.rng.lognormal(mu_ln, sigma_ln))
        return max(7, min(90, lead_time))  # Bound between 7 and 90 days

    def generate_facilities(self) -> List[Dict[str, Any]]:
        """Returns facility master records."""
        return [
            {
                "code": f["code"],
                "name": f["name"],
                "facility_type": f["facility_type"],
                "region": f["region"],
                "zone": f.get("zone"),
                "woreda": f.get("woreda"),
                "latitude": f.get("latitude"),
                "longitude": f.get("longitude"),
                "catchment_population": f.get("catchment_population"),
                "is_active": True,
            }
            for f in self.facilities
        ]

    def generate_medicines(self) -> List[Dict[str, Any]]:
        """Returns medicine master records."""
        return [
            {
                "code": m["code"],
                "name": m["name"],
                "category": m["category"],
                "dosage_form": m["dosage_form"],
                "strength": m["strength"],
                "unit_of_measure": m["unit_of_measure"],
                "is_essential": True,
                "vital_classification": m["vital_classification"],
                "minimum_stock_level": m["base_monthly_demand"] * 0.5,
                "reorder_point": m["base_monthly_demand"] * 1.5,
                "lead_time_days": 30,
            }
            for m in self.medicines
        ]

    def generate_full_dataset(self) -> Dict[str, Any]:
        """
        Generates the complete synthetic dataset:
        - facilities, medicines, batches, inventory snapshots, transactions

        Returns dict with keys: facilities, medicines, batches, inventories, transactions,
        anomalies_injected, metadata
        """
        start_date = date.today() - timedelta(days=self.num_months * 30)
        facilities = self.generate_facilities()
        medicines = self.generate_medicines()

        all_batches: List[Dict] = []
        all_inventories: List[Dict] = []
        all_transactions: List[Dict] = []
        batch_counter = 0

        for facility in self.facilities:
            fac_code = facility["code"]
            demand_mult = facility["demand_multiplier"]

            for med_template in self.medicines:
                med_code = med_template["code"]
                base_demand = med_template["base_monthly_demand"]
                cv = med_template["demand_cv"]
                category = med_template["demand_category"]
                shelf_min, shelf_max = med_template["shelf_life_months"]
                unit_cost = med_template["unit_cost_etb"]

                # Simulation state
                stock_on_hand = 0.0
                active_batches: List[Dict] = []  # Ordered by expiry (FEFO)
                total_consumed_lifetime = 0.0
                months_with_data = 0

                for month_offset in range(self.num_months):
                    current_date = start_date + timedelta(days=month_offset * 30)
                    calendar_month = current_date.month

                    # ─── Supply: Replenishment every 2-4 months or when low ───
                    should_reorder = (
                        stock_on_hand < base_demand * demand_mult * 1.5
                        or month_offset % 3 == 0
                    )

                    if should_reorder:
                        lead_time = self._generate_lead_time_days()
                        receipt_date = current_date + timedelta(days=lead_time)

                        # Order quantity: 2-4 months of demand
                        order_months = int(self.rng.integers(2, 5))
                        order_qty = int(base_demand * demand_mult * order_months)
                        order_qty = max(50, order_qty)

                        shelf_life = int(self.rng.integers(shelf_min, shelf_max + 1))
                        mfg_date = receipt_date - timedelta(days=int(self.rng.integers(30, 120)))
                        exp_date = mfg_date + timedelta(days=shelf_life * 30)

                        batch_counter += 1
                        batch_no = f"BN-{fac_code[-5:]}-{med_code[-4:]}-{batch_counter:05d}"

                        batch_record = {
                            "facility_code": fac_code,
                            "medicine_code": med_code,
                            "batch_number": batch_no,
                            "manufacturing_date": mfg_date.isoformat(),
                            "expiry_date": exp_date.isoformat(),
                            "quantity_initial": order_qty,
                            "quantity_remaining": order_qty,
                            "unit_cost_etb": round(unit_cost * (1 + self.rng.uniform(-0.05, 0.10)), 2),
                            "status": "Active",
                        }
                        all_batches.append(batch_record)
                        active_batches.append(batch_record)
                        stock_on_hand += order_qty

                        # RECEIPT transaction
                        all_transactions.append({
                            "facility_code": fac_code,
                            "medicine_code": med_code,
                            "batch_number": batch_no,
                            "transaction_type": "RECEIPT",
                            "quantity": order_qty,
                            "transaction_date": receipt_date.isoformat(),
                            "reference_number": f"STV-{batch_counter:06d}",
                            "notes": f"EPSS replenishment, lead time {lead_time} days",
                        })

                    # Sort active batches by expiry (FEFO)
                    active_batches.sort(key=lambda b: b["expiry_date"])

                    # ─── Demand: Monthly consumption ───
                    demand = self._generate_demand(
                        base_demand, cv, demand_mult, category, calendar_month
                    )

                    # Stockout censoring: actual dispensed = min(demand, available)
                    actual_dispensed = min(demand, stock_on_hand)
                    stockout_days = 0

                    if demand > stock_on_hand:
                        # Partial fulfillment → some stockout days
                        ratio = stock_on_hand / max(1, demand)
                        stockout_days = int(30 * (1 - ratio))
                        stock_on_hand = 0.0
                    else:
                        stock_on_hand -= actual_dispensed

                    # FEFO drawdown across batches
                    remaining_to_draw = actual_dispensed
                    for batch in active_batches[:]:
                        if remaining_to_draw <= 0:
                            break
                        draw = min(remaining_to_draw, batch["quantity_remaining"])
                        batch["quantity_remaining"] -= draw
                        remaining_to_draw -= draw
                        if batch["quantity_remaining"] <= 0:
                            batch["status"] = "Depleted"
                            active_batches.remove(batch)

                    if actual_dispensed > 0:
                        all_transactions.append({
                            "facility_code": fac_code,
                            "medicine_code": med_code,
                            "batch_number": active_batches[0]["batch_number"] if active_batches else "",
                            "transaction_type": "DISPENSATION",
                            "quantity": actual_dispensed,
                            "transaction_date": (current_date + timedelta(days=15)).isoformat(),
                            "reference_number": None,
                            "notes": f"Monthly consumption (demand={demand}, stockout_days={stockout_days})",
                        })
                        total_consumed_lifetime += actual_dispensed
                        months_with_data += 1

                    # Expire batches past their date
                    for batch in active_batches[:]:
                        if date.fromisoformat(batch["expiry_date"]) <= current_date:
                            expired_qty = batch["quantity_remaining"]
                            batch["status"] = "Expired"
                            stock_on_hand -= expired_qty
                            stock_on_hand = max(0.0, stock_on_hand)
                            active_batches.remove(batch)

                            if expired_qty > 0:
                                all_transactions.append({
                                    "facility_code": fac_code,
                                    "medicine_code": med_code,
                                    "batch_number": batch["batch_number"],
                                    "transaction_type": "EXPIRY",
                                    "quantity": expired_qty,
                                    "transaction_date": current_date.isoformat(),
                                    "reference_number": None,
                                    "notes": f"Batch expired on {batch['expiry_date']}",
                                })

                # Final inventory snapshot
                amc = total_consumed_lifetime / max(1, months_with_data)
                mos = stock_on_hand / max(0.01, amc)
                stock_status = (
                    "Stockout" if stock_on_hand <= 0
                    else "Understocked" if mos < 2
                    else "Overstocked" if mos > 6
                    else "Adequate"
                )

                all_inventories.append({
                    "facility_code": fac_code,
                    "medicine_code": med_code,
                    "current_stock": round(stock_on_hand, 2),
                    "usable_stock": round(stock_on_hand, 2),
                    "average_monthly_consumption": round(amc, 2),
                    "months_of_stock": round(mos, 2),
                    "stock_status": stock_status,
                })

        # ─── Inject controlled anomalies ───
        self._inject_anomalies(all_batches, all_inventories, all_transactions)

        return {
            "facilities": facilities,
            "medicines": medicines,
            "batches": all_batches,
            "inventories": all_inventories,
            "transactions": all_transactions,
            "anomalies_injected": self.anomalies_injected,
            "metadata": {
                "num_facilities": self.num_facilities,
                "num_medicines": len(self.medicines),
                "num_months": self.num_months,
                "num_batches": len(all_batches),
                "num_transactions": len(all_transactions),
                "num_inventory_records": len(all_inventories),
                "anomaly_rate": self.anomaly_rate,
                "anomalies_count": len(self.anomalies_injected),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
        }

    def _inject_anomalies(
        self,
        batches: List[Dict],
        inventories: List[Dict],
        transactions: List[Dict],
    ) -> None:
        """Deterministically injects known anomalies for DQI benchmarking."""
        if self.anomaly_rate <= 0 or not batches:
            return

        num_batch_anomalies = max(1, int(len(batches) * self.anomaly_rate))
        num_tx_anomalies = max(1, int(len(transactions) * self.anomaly_rate * 0.5))

        # Select random batch indices for anomaly injection
        batch_indices = self.rng.choice(len(batches), size=min(num_batch_anomalies, len(batches)), replace=False)

        for idx in batch_indices:
            anomaly_type = random.choice(["negative_stock", "expired_active", "quantity_overflow", "missing_batch_number"])
            batch = batches[idx]

            if anomaly_type == "negative_stock":
                original = batch["quantity_remaining"]
                batch["quantity_remaining"] = -abs(int(self.rng.integers(10, 200)))
                self.anomalies_injected.append({
                    "type": "negative_stock",
                    "entity": "batch",
                    "batch_number": batch["batch_number"],
                    "facility_code": batch["facility_code"],
                    "original_value": original,
                    "injected_value": batch["quantity_remaining"],
                })

            elif anomaly_type == "expired_active":
                batch["status"] = "Active"
                past_date = date.today() - timedelta(days=int(self.rng.integers(30, 365)))
                batch["expiry_date"] = past_date.isoformat()
                self.anomalies_injected.append({
                    "type": "expired_active",
                    "entity": "batch",
                    "batch_number": batch["batch_number"],
                    "facility_code": batch["facility_code"],
                    "injected_expiry": batch["expiry_date"],
                })

            elif anomaly_type == "quantity_overflow":
                batch["quantity_remaining"] = batch["quantity_initial"] + int(self.rng.integers(100, 500))
                self.anomalies_injected.append({
                    "type": "quantity_overflow",
                    "entity": "batch",
                    "batch_number": batch["batch_number"],
                    "facility_code": batch["facility_code"],
                })

            elif anomaly_type == "missing_batch_number":
                original_bn = batch["batch_number"]
                batch["batch_number"] = ""
                self.anomalies_injected.append({
                    "type": "missing_batch_number",
                    "entity": "batch",
                    "batch_number": original_bn,
                    "facility_code": batch["facility_code"],
                })

        # Inject reconciliation mismatches into inventories
        num_inv_anomalies = max(1, int(len(inventories) * self.anomaly_rate * 0.5))
        inv_indices = self.rng.choice(len(inventories), size=min(num_inv_anomalies, len(inventories)), replace=False)

        for idx in inv_indices:
            inv = inventories[idx]
            original_stock = inv["current_stock"]
            # Skew the stock away from batch sum
            inv["current_stock"] = round(float(original_stock + int(self.rng.integers(50, 500))), 2)
            self.anomalies_injected.append({
                "type": "reconciliation_mismatch",
                "entity": "inventory",
                "facility_code": inv["facility_code"],
                "medicine_code": inv["medicine_code"],
                "original_stock": original_stock,
                "injected_stock": inv["current_stock"],
            })

    def export_batches_csv(self, batches: List[Dict]) -> str:
        """Exports batch records as importable CSV string."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "medicine_code", "batch_number", "expiry_date", "quantity", "unit_cost_etb"
        ])
        writer.writeheader()
        for b in batches:
            writer.writerow({
                "medicine_code": b["medicine_code"],
                "batch_number": b["batch_number"],
                "expiry_date": b["expiry_date"],
                "quantity": b["quantity_remaining"],
                "unit_cost_etb": b.get("unit_cost_etb", 0.0),
            })
        return output.getvalue()

    def export_transactions_csv(self, transactions: List[Dict]) -> str:
        """Exports transaction records as importable CSV string."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "medicine_code", "transaction_type", "quantity",
            "transaction_date", "batch_number", "reference_number", "notes"
        ])
        writer.writeheader()
        for tx in transactions:
            writer.writerow({
                "medicine_code": tx["medicine_code"],
                "transaction_type": tx["transaction_type"],
                "quantity": tx["quantity"],
                "transaction_date": tx["transaction_date"],
                "batch_number": tx.get("batch_number", ""),
                "reference_number": tx.get("reference_number", ""),
                "notes": tx.get("notes", ""),
            })
        return output.getvalue()

    def get_facility_batches(self, dataset: Dict, facility_code: str) -> List[Dict]:
        """Filters batches for a specific facility."""
        return [b for b in dataset["batches"] if b["facility_code"] == facility_code]

    def get_facility_transactions(self, dataset: Dict, facility_code: str) -> List[Dict]:
        """Filters transactions for a specific facility."""
        return [t for t in dataset["transactions"] if t["facility_code"] == facility_code]
