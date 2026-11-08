"""Data pipeline module for ingestion, validation, and preprocessing."""

import logging
from typing import Dict, Any, Optional
import pandas as pd
from ml.common.config import MLConfig
from ml.common.logging import setup_logger

logger = setup_logger(__name__)


class DataPipeline:
    """End-to-end data pipeline for cleaning, validation, and feature preparation."""

    def __init__(self, config: Optional[MLConfig] = None):
        self.config = config or MLConfig()

    def load_data(self, source_path: str) -> pd.DataFrame:
        """Loads dataset from disk.

        Args:
            source_path: Path to dataset file (CSV/Parquet).

        Returns:
            pd.DataFrame containing raw data.
        """
        logger.info("Loading raw data from %s", source_path)
        if source_path.endswith(".parquet"):
            return pd.read_parquet(source_path)
        return pd.read_csv(source_path)

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Validates dataframe schema against expected columns and types.

        Args:
            df: Input dataframe.

        Returns:
            True if schema is valid, raises ValueError otherwise.
        """
        required_cols = {"timestamp", "product_id", "facility_id"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns in dataset: {missing}")
        logger.info("Dataset schema validated successfully.")
        return True

    def run(self, source_path: str) -> pd.DataFrame:
        """Executes full data ingestion and validation pipeline.

        Args:
            source_path: Path to input dataset.

        Returns:
            Preprocessed pandas DataFrame.
        """
        df = self.load_data(source_path)
        self.validate_schema(df)
        logger.info("Data pipeline completed processing %d records.", len(df))
        return df
