"""
Azubi-Mate Core Module
Contains shared data types, interfaces, base classes, exceptions, and configuration.
"""
from .models import CoreModel
from .dto import BaseDTO
from .interfaces import BaseEngine
from .exceptions import AzubiMateException, ConfigurationError
from .config import config, AppConfig

__all__ = [
    "CoreModel",
    "BaseDTO",
    "BaseEngine",
    "AzubiMateException",
    "ConfigurationError",
    "config",
    "AppConfig",
]