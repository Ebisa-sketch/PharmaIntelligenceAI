"""
PharmaIntelligence AI - Database Initialization Script

Creates all core tables, constraints, relationships, and indices defined in
the SQLAlchemy ORM models. Works with both PostgreSQL and SQLite.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

# Ensure backend root is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.core.config import settings
from app.database.base import Base
from app.database.connection import engine
import app.models  # Registers all 13 models on Base.metadata

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("db_init")


def initialize_database(drop_first: bool = False) -> None:
    """Create all tables in the database using Base.metadata."""
    logger.info("Initializing database with URL: %s", settings.DATABASE_URL.split("@")[-1])

    if drop_first:
        logger.warning("Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("Tables dropped successfully.")

    logger.info("Creating all tables, constraints, and indexes...")
    Base.metadata.create_all(bind=engine)

    tables = list(Base.metadata.tables.keys())
    logger.info("Successfully initialized %d tables:", len(tables))
    for idx, table_name in enumerate(sorted(tables), start=1):
        tbl = Base.metadata.tables[table_name]
        cols = len(tbl.columns)
        fks = len(tbl.foreign_keys)
        indexes = len(tbl.indexes)
        constraints = len(tbl.constraints)
        logger.info(
            "  %2d. %-32s (%d columns, %d foreign keys, %d indexes, %d constraints)",
            idx, table_name, cols, fks, indexes, constraints
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize PharmaIntelligence AI Database")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all existing tables before recreating (Destructive!)",
    )
    args = parser.parse_args()
    initialize_database(drop_first=args.drop)


if __name__ == "__main__":
    main()
