# backend/dependencies.py
import logging
import os
from azubi_mate_core import logger as core_logger, LLMProvider
from backend.ai import OpenAIProvider, OllamaProvider, GeminiProvider, MockLLMProvider

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