"""Logging configuration and utilities for ML pipelines."""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = "PharmaIntelligenceAI.ML",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """Configures and returns a structured logger.

    Args:
        name: Logger name.
        level: Logging level (e.g. logging.INFO, logging.DEBUG).
        log_file: Optional path to write log output to a file.

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
