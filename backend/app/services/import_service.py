import csv
import hashlib
import io
import json
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd
from sqlalchemy.orm import Session

from app.models.facility import Facility
from app.models.medicine import Medicine
from app.models.batch import Batch
from app.models.inventory import Inventory
from app.models.transaction import InventoryTransaction
from app.models.data_import import DataImport
from app.models.data_quality import DataQualityIssue
from app.models.audit_log import AuditLog
from app.core.exceptions import DataQualityValidationError


class ImportService:
    def __init__(self, db: Session):
        self.db = db

    def compute_sha256(self, file_bytes: bytes) -> str:
        """Computes SHA-256 hash string for raw file bytes."""
        hasher = hashlib.sha256()
        hasher.update(file_bytes)
        return hasher.hexdigest()

    def parse_file_to_records(
        self, file_bytes: bytes, filename: str
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Parses CSV or Excel (.xlsx) file bytes into a list of normalized row dictionaries."""
        lower_name = filename.lower()
        if lower_name.endswith(".xlsx") or lower_name.endswith(".xls"):
            try:
                df = pd.read_excel(io.BytesIO(file_bytes))
                df = df.where(pd.notnull(df), None)
                # Normalize column headers: strip whitespace, lowercase, replace spaces with underscores
                df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
                return df.to_dict(orient="records"), list(df.columns)
            except Exception as exc:
                raise DataQualityValidationError(f"Failed to parse Excel file '{filename}': {str(exc)}")
        else:
            # Assume CSV / TSV text
            try:
                text_content = file_bytes.decode("utf-8-sig")
            except UnicodeDecodeError:
                try:
                    text_content = file_bytes.decode("latin-1")
                except Exception as exc:
                    raise DataQualityValidationError(f"Invalid file encoding. Please supply a UTF-8 encoded file: {str(exc)}")

            # Sniff delimiter (comma, semicolon, tab)
            sample = text_content[:2048]
            delimiter = ","
            if sample:
                try:
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(sample, delimiters=[",", ";", "\t", "|"])
                    delimiter = dialect.delimiter
                except Exception:
                    delimiter = ","

            reader = csv.DictReader(io.StringIO(text_content), delimiter=delimiter)
            if not reader.fieldnames:
                raise DataQualityValidationError("Uploaded file has no headers or is empty.")

            normalized_headers = [str(h).strip().lower().replace(" ", "_") for h in reader.fieldnames if h]
            records: List[Dict[str, Any]] = []

            for row in reader:
                norm_row = {}
                for k, v in row.items():
                    if k is not None:
                        clean_key = str(k).strip().lower().replace(" ", "_")
                        norm_row[clean_key] = v.strip() if isinstance(v, str) else v
                records.append(norm_row)

            return records, normalized_headers

    def preview_import(
        self, file_bytes: bytes, filename: str, preview_limit: int = 5
    ) -> Dict[str, Any]:
        """Provides preliminary structural inspection and validation without committing to DB."""
        records, headers = self.parse_file_to_records(file_bytes, filename)
        total_rows = len(records)
        sample_rows = records[:preview_limit]

        preview_issues = []
        valid_estimate = 0
        rejected_estimate = 0

        # Quick validation of first sample rows
        for idx, row in enumerate(records[:100], start=1):
            med_code = row.get("medicine_code") or row.get("code")
            qty = row.get("quantity") or row.get("current_stock")
            if not med_code:
                rejected_estimate += 1
                if len(preview_issues) < 10:
                    preview_issues.append({"row": idx, "error": "Missing medicine_code"})
                continue
            try:
                if qty is not None and float(qty) < 0:
                    rejected_estimate += 1
                    if len(preview_issues) < 10:
                        preview_issues.append({"row": idx, "error": f"Negative quantity ({qty})"})
                    continue
            except (ValueError, TypeError):
                rejected_estimate += 1
                if len(preview_issues) < 10:
                    preview_issues.append({"row": idx, "error": f"Invalid numeric quantity '{qty}'"})
                continue

            valid_estimate += 1

        sample_total = valid_estimate + rejected_estimate
        score = (valid_estimate / sample_total * 100.0) if sample_total > 0 else 100.0

        return {
            "filename": filename,
            "total_rows": total_rows,
            "estimated_valid_rows": int(total_rows * (valid_estimate / max(1, sample_total))),
            "estimated_rejected_rows": int(total_rows * (rejected_estimate / max(1, sample_total))),
            "preliminary_dq_score": round(score, 1),
            "detected_headers": headers,
            "sample_rows": sample_rows,
            "preview_issues": preview_issues,
        }

    def import_inventory_batches(
        self,
        file_bytes: bytes,
        filename: str,
        facility_id: int,
        user_id: int,
    ) -> Dict[str, Any]:
        """
        Processes batch inventory upload:
        Expected columns: medicine_code, batch_number, expiry_date, quantity, [unit_cost_etb, reorder_level]
        """
        facility = self.db.get(Facility, facility_id)
        if not facility:
            raise DataQualityValidationError(f"Target facility ID {facility_id} does not exist.")

        file_hash = self.compute_sha256(file_bytes)
        records, headers = self.parse_file_to_records(file_bytes, filename)
        total_rows = len(records)

        # Create DataImport job record
        data_import = DataImport(
            facility_id=facility_id,
            uploaded_by_user_id=user_id,
            filename=filename,
            file_hash_sha256=file_hash,
            total_rows=total_rows,
            valid_rows=0,
            rejected_rows=0,
            dq_score=100.0,
            status="PROCESSING",
        )
        self.db.add(data_import)
        self.db.flush()

        valid_rows = 0
        rejected_rows = 0
        issues_to_persist = []
        today = date.today()

        # Cache medicines lookup map for high performance
        medicines = {m.code.upper(): m for m in self.db.query(Medicine).all()}

        for row_idx, row in enumerate(records, start=1):
            med_code_raw = str(row.get("medicine_code") or row.get("code") or "").strip().upper()
            batch_no_raw = str(row.get("batch_number") or row.get("batch") or "").strip()
            expiry_str = str(row.get("expiry_date") or row.get("expiration_date") or "").strip()
            qty_raw = row.get("quantity") or row.get("current_stock") or row.get("quantity_remaining")
            cost_raw = row.get("unit_cost_etb") or row.get("cost") or 0.0

            # Rule A02: Mandatory attributes
            if not med_code_raw or not batch_no_raw or not expiry_str or qty_raw is None:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        issue_type="MISSING_MANDATORY_FIELD",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="medicine_code/batch_number/expiry_date",
                        description=f"Row {row_idx}: Missing required fields.",
                    )
                )
                continue

            # Foreign key verification
            medicine = medicines.get(med_code_raw)
            if not medicine:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        issue_type="UNKNOWN_MEDICINE_CODE",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="medicine_code",
                        description=f"Row {row_idx}: Medicine code '{med_code_raw}' not found in NEML catalogue.",
                    )
                )
                continue

            # Quantity and cost type conversion
            try:
                quantity = float(qty_raw)
                unit_cost = float(cost_raw) if cost_raw else 0.0
            except (ValueError, TypeError):
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="INVALID_NUMERIC_FORMAT",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="quantity",
                        description=f"Row {row_idx}: Non-numeric quantity value '{qty_raw}'.",
                    )
                )
                continue

            # Non-negativity check (Rule A04)
            if quantity < 0:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="NEGATIVE_QUANTITY",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="quantity",
                        description=f"Row {row_idx}: Quantity cannot be negative ({quantity}).",
                    )
                )
                continue

            # Date normalization (Rule A03)
            expiry_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
                try:
                    expiry_date = datetime.strptime(expiry_str, fmt).date()
                    break
                except ValueError:
                    continue

            if not expiry_date:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="INVALID_DATE_FORMAT",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="expiry_date",
                        description=f"Row {row_idx}: Unparseable date format '{expiry_str}'. Expected YYYY-MM-DD.",
                    )
                )
                continue

            # Check if batch is already expired at import time
            batch_status = "Active"
            if expiry_date < today:
                batch_status = "Expired"
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="EXPIRED_BATCH_INGESTED",
                        severity="WARNING",
                        row_number=row_idx,
                        field_name="expiry_date",
                        description=f"Row {row_idx}: Ingested batch '{batch_no_raw}' expired on {expiry_date}.",
                    )
                )

            # Insert or update Batch
            batch = self.db.query(Batch).filter(
                Batch.facility_id == facility_id,
                Batch.medicine_id == medicine.id,
                Batch.batch_number == batch_no_raw,
            ).first()

            if not batch:
                batch = Batch(
                    facility_id=facility_id,
                    medicine_id=medicine.id,
                    batch_number=batch_no_raw,
                    expiry_date=expiry_date,
                    quantity_initial=quantity,
                    quantity_remaining=quantity,
                    unit_cost_etb=unit_cost,
                    status=batch_status,
                )
                self.db.add(batch)
            else:
                batch.quantity_remaining += quantity
                batch.unit_cost_etb = unit_cost
                batch.status = batch_status

            # Reconcile master Inventory record
            inventory = self.db.query(Inventory).filter(
                Inventory.facility_id == facility_id,
                Inventory.medicine_id == medicine.id,
            ).first()

            if not inventory:
                inventory = Inventory(
                    facility_id=facility_id,
                    medicine_id=medicine.id,
                    current_stock=quantity if batch_status == "Active" else 0.0,
                    usable_stock=quantity if batch_status == "Active" else 0.0,
                    reserved_stock=0.0,
                    stock_status="Adequate" if quantity > 0 else "Stockout",
                    last_counted_date=datetime.now(timezone.utc),
                )
                self.db.add(inventory)
            else:
                if batch_status == "Active":
                    inventory.current_stock += quantity
                    inventory.usable_stock += quantity
                inventory.last_counted_date = datetime.now(timezone.utc)
                inventory.stock_status = "Adequate" if inventory.current_stock > 0 else "Stockout"

            valid_rows += 1

        # Calculate DQI score for this import job
        total_attempted = valid_rows + rejected_rows
        dq_score = round((valid_rows / total_attempted * 100.0) if total_attempted > 0 else 100.0, 1)

        # Update DataImport record
        data_import.valid_rows = valid_rows
        data_import.rejected_rows = rejected_rows
        data_import.dq_score = dq_score
        data_import.status = "COMPLETED" if rejected_rows == 0 else "PARTIAL_SUCCESS"

        # Bulk add quality issues
        if issues_to_persist:
            self.db.add_all(issues_to_persist)

        # Add AuditLog
        audit = AuditLog(
            user_id=user_id,
            action="IMPORT_INVENTORY_BATCHES",
            entity_type="data_imports",
            entity_id=data_import.id,
            details=f"Imported {filename}: {valid_rows}/{total_rows} valid rows, DQ Score: {dq_score}%.",
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(data_import)

        return {
            "import_id": data_import.id,
            "facility_id": facility_id,
            "filename": filename,
            "total_rows": total_rows,
            "valid_rows": valid_rows,
            "rejected_rows": rejected_rows,
            "dq_score": dq_score,
            "status": data_import.status,
            "issues_count": len(issues_to_persist),
        }

    def import_transactions(
        self,
        file_bytes: bytes,
        filename: str,
        facility_id: int,
        user_id: int,
    ) -> Dict[str, Any]:
        """
        Processes bin-card inventory transaction ledger upload:
        Expected columns: medicine_code, transaction_type, quantity, transaction_date, [batch_number, reference_number, notes]
        """
        facility = self.db.get(Facility, facility_id)
        if not facility:
            raise DataQualityValidationError(f"Target facility ID {facility_id} does not exist.")

        file_hash = self.compute_sha256(file_bytes)
        records, headers = self.parse_file_to_records(file_bytes, filename)
        total_rows = len(records)

        data_import = DataImport(
            facility_id=facility_id,
            uploaded_by_user_id=user_id,
            filename=filename,
            file_hash_sha256=file_hash,
            total_rows=total_rows,
            valid_rows=0,
            rejected_rows=0,
            dq_score=100.0,
            status="PROCESSING",
        )
        self.db.add(data_import)
        self.db.flush()

        valid_rows = 0
        rejected_rows = 0
        issues_to_persist = []
        medicines = {m.code.upper(): m for m in self.db.query(Medicine).all()}

        VALID_TYPES = {
            "RECEIPT", "DISPENSATION", "ISSUE", "ADJUSTMENT_POSITIVE",
            "ADJUSTMENT_NEGATIVE", "TRANSFER_IN", "TRANSFER_OUT", "WASTAGE", "EXPIRY"
        }

        for row_idx, row in enumerate(records, start=1):
            med_code_raw = str(row.get("medicine_code") or row.get("code") or "").strip().upper()
            tx_type_raw = str(row.get("transaction_type") or row.get("type") or "").strip().upper()
            qty_raw = row.get("quantity")
            date_str = str(row.get("transaction_date") or row.get("date") or "").strip()
            batch_no = str(row.get("batch_number") or row.get("batch") or "").strip() or None
            ref_num = str(row.get("reference_number") or row.get("reference") or row.get("voucher") or "").strip() or None
            notes = str(row.get("notes") or "").strip() or None

            # Validation
            if not med_code_raw or not tx_type_raw or qty_raw is None or not date_str:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        issue_type="MISSING_MANDATORY_FIELD",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="medicine_code/transaction_type/quantity/transaction_date",
                        description=f"Row {row_idx}: Missing mandatory transaction fields.",
                    )
                )
                continue

            medicine = medicines.get(med_code_raw)
            if not medicine:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        issue_type="UNKNOWN_MEDICINE_CODE",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="medicine_code",
                        description=f"Row {row_idx}: Unknown medicine code '{med_code_raw}'.",
                    )
                )
                continue

            if tx_type_raw not in VALID_TYPES:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="INVALID_TRANSACTION_TYPE",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="transaction_type",
                        description=f"Row {row_idx}: Invalid transaction type '{tx_type_raw}'.",
                    )
                )
                continue

            try:
                quantity = float(qty_raw)
            except (ValueError, TypeError):
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="INVALID_NUMERIC_FORMAT",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="quantity",
                        description=f"Row {row_idx}: Invalid quantity value '{qty_raw}'.",
                    )
                )
                continue

            if quantity <= 0:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="NON_POSITIVE_QUANTITY",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="quantity",
                        description=f"Row {row_idx}: Transaction quantity must be > 0 ({quantity}).",
                    )
                )
                continue

            # Parse date
            tx_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                try:
                    tx_date = datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
                    break
                except ValueError:
                    continue

            if not tx_date:
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="INVALID_DATE_FORMAT",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="transaction_date",
                        description=f"Row {row_idx}: Cannot parse date '{date_str}'.",
                    )
                )
                continue

            # Future date check
            if tx_date > datetime.now(timezone.utc):
                rejected_rows += 1
                issues_to_persist.append(
                    DataQualityIssue(
                        import_id=data_import.id,
                        facility_id=facility_id,
                        medicine_id=medicine.id,
                        issue_type="FUTURE_TRANSACTION_DATE",
                        severity="CRITICAL",
                        row_number=row_idx,
                        field_name="transaction_date",
                        description=f"Row {row_idx}: Transaction date {tx_date.date()} is in the future.",
                    )
                )
                continue

            # Find batch if batch_no provided
            batch_id = None
            if batch_no:
                batch = self.db.query(Batch).filter(
                    Batch.facility_id == facility_id,
                    Batch.medicine_id == medicine.id,
                    Batch.batch_number == batch_no,
                ).first()
                if batch:
                    batch_id = batch.id

            # Create InventoryTransaction record
            tx = InventoryTransaction(
                facility_id=facility_id,
                medicine_id=medicine.id,
                batch_id=batch_id,
                transaction_type=tx_type_raw,
                quantity=quantity,
                transaction_date=tx_date,
                reference_number=ref_num,
                notes=notes,
                created_by=user_id,
                import_id=data_import.id,
            )
            self.db.add(tx)
            valid_rows += 1

        total_attempted = valid_rows + rejected_rows
        dq_score = round((valid_rows / total_attempted * 100.0) if total_attempted > 0 else 100.0, 1)

        data_import.valid_rows = valid_rows
        data_import.rejected_rows = rejected_rows
        data_import.dq_score = dq_score
        data_import.status = "COMPLETED" if rejected_rows == 0 else "PARTIAL_SUCCESS"

        if issues_to_persist:
            self.db.add_all(issues_to_persist)

        audit = AuditLog(
            user_id=user_id,
            action="IMPORT_TRANSACTIONS",
            entity_type="data_imports",
            entity_id=data_import.id,
            details=f"Imported transactions {filename}: {valid_rows}/{total_rows} valid rows, DQ Score: {dq_score}%.",
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(data_import)

        return {
            "import_id": data_import.id,
            "facility_id": facility_id,
            "filename": filename,
            "total_rows": total_rows,
            "valid_rows": valid_rows,
            "rejected_rows": rejected_rows,
            "dq_score": dq_score,
            "status": data_import.status,
            "issues_count": len(issues_to_persist),
        }
