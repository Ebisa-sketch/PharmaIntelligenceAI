"""
PharmaIntelligence AI - Dataset Schema Validation Tool

Validates tabular records against predefined JSON schemas located in data/schemas/.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required. Please install pandas.", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    print("Error: jsonschema is required. Please install jsonschema.", file=sys.stderr)
    sys.exit(1)


def validate_records(data_path: Path, schema_path: Path, max_errors: int = 20) -> bool:
    if not schema_path.exists():
        print(f"[!] Schema not found at {schema_path}", file=sys.stderr)
        return False
    if not data_path.exists():
        print(f"[!] Data file not found at {data_path}", file=sys.stderr)
        return False

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validator = Draft202012Validator(schema)

    if data_path.suffix.lower() == ".csv":
        df = pd.read_csv(data_path)
    elif data_path.suffix.lower() in [".parquet", ".pq"]:
        df = pd.read_parquet(data_path)
    else:
        print(f"[!] Unsupported format: {data_path.suffix}", file=sys.stderr)
        return False

    records = df.to_dict(orient="records")
    print(f"[*] Validating {len(records)} records from {data_path.name} against {schema_path.name}...")

    error_count = 0
    for idx, row in enumerate(records):
        # Filter out NaN/None entries that might violate schema nullability
        cleaned_row = {k: v for k, v in row.items() if pd.notnull(v)}
        for error in validator.iter_errors(cleaned_row):
            error_count += 1
            print(f"  [Row {idx+1}] {error.message} (Field: {'.'.join(str(p) for p in error.path)})")
            if error_count >= max_errors:
                print(f"[!] Reached max error threshold ({max_errors}). Validation aborted.")
                return False

    if error_count == 0:
        print(f"[✓] Validation successful: All {len(records)} records comply with schema.")
        return True
    else:
        print(f"[!] Total errors found: {error_count}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Validate dataset records against JSON schema")
    parser.add_argument("--data", required=True, type=Path, help="Path to CSV or Parquet data file")
    parser.add_argument("--schema", required=True, type=Path, help="Path to JSON schema file")
    parser.add_argument("--max-errors", type=int, default=20, help="Maximum number of errors to report")
    args = parser.parse_args()

    success = validate_records(args.data, args.schema, args.max_errors)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
