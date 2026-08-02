# azubi_mate_core/__init__.py
"""
Azubi-Mate Core Module
Contains shared data types, interfaces, base classes, exceptions, and configuration.
"""
from .models import CoreModel
from .dto import BaseDTO
from .interfaces import BaseEngine
from .exceptions import (
    AzubiMateException,
    ConfigurationError,
    NotFoundError,
    ValidationException,
)
from .config import config, AppConfig, logger, setup_logging

__all__ = [
    "CoreModel",
    "BaseDTO",
    "BaseEngine",
    "AzubiMateException",
    "ConfigurationError",
    "NotFoundError",
    "ValidationException",
    "config",
    "AppConfig",
    "logger",
    "setup_logging",
]