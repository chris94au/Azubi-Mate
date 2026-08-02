# tests/test_phase_1.py
import pytest
from azubi_mate_core import (
    CoreModel,
    BaseDTO,
    BaseEngine,
    AzubiMateException,
    ConfigurationError,
    config,
    logger,
)

class DummyEngine(BaseEngine):
    def initialize(self) -> None:
        pass

    def get_status(self) -> dict:
        return {"status": "active"}

def test_core_models_and_dtos() -> None:
    model = CoreModel()
    assert model is not None
    dto = BaseDTO()
    assert dto is not None

def test_interface_implementation() -> None:
    engine = DummyEngine()
    engine.initialize()
    status = engine.get_status()
    assert status["status"] == "active"

def test_exceptions() -> None:
    exc = AzubiMateException("Base error")
    assert exc.message == "Base error"
    
    cfg_exc = ConfigurationError("Config error")
    assert cfg_exc.message == "Config error"
    assert isinstance(cfg_exc, AzubiMateException)

def test_config_and_logging() -> None:
    assert config.app_name is not None
    assert logger is not None