"""
PharmaIntelligence AI - Dataset Inspection Tool

Reads tabular datasets (CSV / Parquet) and generates statistical summaries,
missingness profiles, cardinality distribution, and initial data health diagnostics.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required to run inspect_dataset.py. Please install pandas.", file=sys.stderr)
    sys.exit(1)


def inspect_file(filepath: Path) -> dict:
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    print(f"[*] Loading dataset: {filepath}")
    if filepath.suffix.lower() == ".csv":
        df = pd.read_csv(filepath)
    elif filepath.suffix.lower() in [".parquet", ".pq"]:
        df = pd.read_parquet(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

    row_count, col_count = df.shape
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    summary = {
        "file_path": str(filepath.resolve()),
        "rows": row_count,
        "columns": col_count,
        "memory_mb": round(memory_mb, 2),
        "column_profiles": {}
    }

    print(f"[✓] Dimensions: {row_count:,} rows × {col_count} columns ({memory_mb:.2f} MB)")
    print("-" * 70)

    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        null_pct = round((null_count / row_count) * 100, 2) if row_count > 0 else 0
        unique_vals = int(df[col].nunique(dropna=True))
        dtype_str = str(df[col].dtype)

        summary["column_profiles"][col] = {
            "dtype": dtype_str,
            "null_count": null_count,
            "null_pct": null_pct,
            "unique_values": unique_vals,
        }

        print(f"• {col:<25} | {dtype_str:<10} | Nulls: {null_count:>6} ({null_pct:>5.1f}%) | Unique: {unique_vals:>6}")

    print("-" * 70)
    return summary


def main():
    parser = argparse.ArgumentParser(description="Inspect dataset contents and health metrics")
    parser.add_argument("path", type=Path, help="Path to CSV or Parquet file")
    parser.add_argument("--json", action="store_true", help="Output summary in JSON format")
    args = parser.parse_args()

    try:
        report = inspect_file(args.path)
        if args.json:
            print(json.dumps(report, indent=2))
    except Exception as exc:
        print(f"[!] Inspection failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
