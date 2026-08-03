# backend/dependencies.py
import logging
import os
from azubi_mate_core import logger as core_logger, LLMProvider, ReportEngineInterface, DocumentEngineInterface
from backend.ai import OpenAIProvider, OllamaProvider, GeminiProvider, MockLLMProvider
from report_engine import ReportEngine
from document_engine import DocumentEngine

def get_logger() -> logging.Logger:
    """Dependency to provide the application logger."""
    return core_logger

def get_llm_provider() -> LLMProvider:
    """Dependency to provide the configured LLM provider based on environment settings."""
    provider_type = os.getenv("AZUBI_LLM_PROVIDER", "mock").lower()
    if provider_type == "openai":
        return OpenAIProvider()
    elif provider_type == "ollama":
        return OllamaProvider()
    elif provider_type == "gemini":
        return GeminiProvider()
    else:
        return MockLLMProvider()

def get_report_engine() -> ReportEngineInterface:
    """Dependency to provide the Report Engine."""
    llm = get_llm_provider()
    engine = ReportEngine(llm)
    engine.initialize()
    return engine

def get_document_engine() -> DocumentEngineInterface:
    """Dependency to provide the Document Engine."""
    engine = DocumentEngine()
    engine.initialize()
    return engine