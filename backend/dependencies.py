# backend/dependencies.py
import logging
from azubi_mate_core import logger as core_logger

def get_logger() -> logging.Logger:
    """Dependency to provide the application logger."""
    return core_logger