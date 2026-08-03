# tests/test_phase_6.py
import pytest
from azubi_mate_core import (
    LLMRequestDTO,
    LLMResponseDTO,
    LLMException,
)
from backend.ai import MockLLMProvider, OllamaProvider, OpenAIProvider, GeminiProvider
from backend.dependencies import get_llm_provider

def test_mock_provider_success():
    provider = MockLLMProvider(canned_response="Test AI Output")
    request = LLMRequestDTO(prompt="Hello AI")
    response = provider.generate(request)

    assert isinstance(response, LLMResponseDTO)
    assert response.text == "Test AI Output"
    assert response.provider == "mock"
    assert response.model == "mock-model"

def test_mock_provider_failure():
    provider = MockLLMProvider(should_fail=True)
    request = LLMRequestDTO(prompt="Will fail")

    with pytest.raises(LLMException) as exc_info:
        provider.generate(request)
    assert "Mock LLM provider error triggered" in str(exc_info.value)

def test_provider_swapping():
    providers = [
        MockLLMProvider(canned_response="Resp 1"),
        MockLLMProvider(canned_response="Resp 2"),
    ]
    request = LLMRequestDTO(prompt="Test prompt")
    
    responses = [p.generate(request) for p in providers]
    assert responses[0].text == "Resp 1"
    assert responses[1].text == "Resp 2"

def test_openai_missing_api_key():
    provider = OpenAIProvider(api_key="")
    request = LLMRequestDTO(prompt="Test")
    with pytest.raises(LLMException) as exc_info:
        provider.generate(request)
    assert "OpenAI API key is missing" in str(exc_info.value)

def test_gemini_missing_api_key():
    provider = GeminiProvider(api_key="")
    request = LLMRequestDTO(prompt="Test")
    with pytest.raises(LLMException) as exc_info:
        provider.generate(request)
    assert "Gemini API key is missing" in str(exc_info.value)

def test_dependency_injection_llm_provider(monkeypatch):
    monkeypatch.setenv("AZUBI_LLM_PROVIDER", "mock")
    provider = get_llm_provider()
    assert isinstance(provider, MockLLMProvider)