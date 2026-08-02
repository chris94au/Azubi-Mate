# azubi_mate_core/__init__.py
"""
Azubi-Mate Core Module
Contains shared data types, interfaces, base classes, exceptions, and configuration.
"""
from .models import CoreModel, KnowledgeItemModel
from .dto import (
    BaseDTO,
    KnowledgeItemDTO,
    KnowledgeSearchQueryDTO,
    ResearchQueryDTO,
    SourceEvaluationDTO,
    ResearchResultDTO,
)
from .interfaces import (
    BaseEngine,
    BaseRepository,
    KnowledgeEngineInterface,
    ResearchEngineInterface,
)
from .exceptions import (
    AzubiMateException,
    ConfigurationError,
    NotFoundError,
    ValidationException,
)
from .config import config, AppConfig, logger, setup_logging

__all__ = [
    "CoreModel",
    "KnowledgeItemModel",
    "BaseDTO",
    "KnowledgeItemDTO",
    "KnowledgeSearchQueryDTO",
    "ResearchQueryDTO",
    "SourceEvaluationDTO",
    "ResearchResultDTO",
    "BaseEngine",
    "BaseRepository",
    "KnowledgeEngineInterface",
    "ResearchEngineInterface",
    "AzubiMateException",
    "ConfigurationError",
    "NotFoundError",
    "ValidationException",
    "config",
    "AppConfig",
    "logger",
    "setup_logging",
]