# backend/ai.py
import os
from typing import Optional
from azubi_mate_core import (
    LLMProvider,
    LLMRequestDTO,
    LLMResponseDTO,
    LLMException,
    logger,
)

class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""

    def __init__(self, canned_response: str = "Mock LLM Response", should_fail: bool = False) -> None:
        self.canned_response = canned_response
        self.should_fail = should_fail

    def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        if self.should_fail:
            raise LLMException("Mock LLM provider error triggered.")
        logger.info(f"MockLLMProvider generating response for prompt: '{request.prompt[:30]}...'")
        return LLMResponseDTO(
            text=self.canned_response,
            model="mock-model",
            provider="mock",
            usage={"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}
        )

class OllamaProvider(LLMProvider):
    """Ollama local LLM provider."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3") -> None:
        self.base_url = base_url
        self.model = model

    def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        logger.info(f"OllamaProvider generating with model {self.model} at {self.base_url}")
        try:
            import httpx
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": request.prompt,
                "system": request.system_prompt,
                "stream": False,
                "options": {
                    "temperature": request.temperature,
                }
            }
            if request.max_tokens:
                payload["options"]["num_predict"] = request.max_tokens

            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload)
                if response.status_code != 200:
                    raise LLMException(f"Ollama API error: {response.text}")
                data = response.json()
                text = data.get("response", "")
                return LLMResponseDTO(
                    text=text,
                    model=self.model,
                    provider="ollama",
                )
        except Exception as e:
            if isinstance(e, LLMException):
                raise e
            logger.error(f"Failed to connect to Ollama: {e}")
            raise LLMException(f"Ollama connection error: {e}")

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        if not self.api_key:
            raise LLMException("OpenAI API key is missing. Set OPENAI_API_KEY environment variable.")
        
        logger.info(f"OpenAIProvider generating with model {self.model}")
        try:
            import httpx
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": request.temperature,
            }
            if request.max_tokens:
                payload["max_tokens"] = request.max_tokens

            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload, headers=headers)
                if response.status_code != 200:
                    raise LLMException(f"OpenAI API error: {response.text}")
                data = response.json()
                text = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                return LLMResponseDTO(
                    text=text,
                    model=self.model,
                    provider="openai",
                    usage=usage,
                )
        except Exception as e:
            if isinstance(e, LLMException):
                raise e
            logger.error(f"OpenAI request failed: {e}")
            raise LLMException(f"OpenAI error: {e}")

class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro") -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model

    def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        if not self.api_key:
            raise LLMException("Gemini API key is missing. Set GEMINI_API_KEY environment variable.")

        logger.info(f"GeminiProvider generating with model {self.model}")
        try:
            import httpx
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            
            contents = []
            parts = []
            if request.system_prompt:
                parts.append({"text": f"System: {request.system_prompt}"})
            parts.append({"text": request.prompt})
            contents.append({"parts": parts})

            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": request.temperature,
                }
            }
            if request.max_tokens:
                payload["generationConfig"]["maxOutputTokens"] = request.max_tokens

            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload)
                if response.status_code != 200:
                    raise LLMException(f"Gemini API error: {response.text}")
                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    raise LLMException("Gemini API returned no candidates.")
                text = candidates[0]["content"]["parts"][0]["text"]
                return LLMResponseDTO(
                    text=text,
                    model=self.model,
                    provider="gemini",
                )
        except Exception as e:
            if isinstance(e, LLMException):
                raise e
            logger.error(f"Gemini request failed: {e}")
            raise LLMException(f"Gemini error: {e}")