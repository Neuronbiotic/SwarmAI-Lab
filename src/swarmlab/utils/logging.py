"""Logging utilities for SwarmAI-Lab."""
from __future__ import annotations

import logging
from typing import Optional


LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(name)s: %(message)s"


def configure_logging(level: int = logging.INFO, name: Optional[str] = None) -> logging.Logger:
    """Configure a named logger with a friendly formatter.

    The function is idempotent; calling it multiple times returns the
    same logger without re-adding handlers.
    """

    logger = logging.getLogger(name or "swarmlab")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)

    logger.propagate = False
    return logger
