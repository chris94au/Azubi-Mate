# tests/test_phase_9.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from azubi_mate_core import (
    LearningPlanRequestDTO,
    LearningPlanDTO,
    LearningProgressUpdateDTO,
    NotFoundError,
)
from backend.ai import MockLLMProvider
from learning_engine import LearningEngine

client = TestClient(app)

def test_learning_engine_initialization():
    llm = MockLLMProvider(canned_response=(
        "Titel: Fachinformatiker Lernplan\n"
        "Zusammenfassung: Test Zusammenfassung\n"
        "THEMA:\n"
        "Name: Python Grundlagen\n"
        "Priorität: high\n"
        "Aktionen: Lesen, Üben\n"
        "---"
    ))
    engine = LearningEngine(llm)
    engine.initialize()
    status = engine.get_status()
    assert status["engine"] == "LearningEngine"
    assert status["status"] == "active"
    assert status["plans_count"] == 0

def test_generate_and_update_learning_plan():
    canned = (
        "Titel: IT-Systemelektroniker Plan\n"
        "Zusammenfassung: Netzwerkfokus\n"
        "THEMA:\n"
        "Name: TCP/IP\n"
        "Priorität: high\n"
        "Aktionen: Protokolle analysieren\n"
        "---"
    )
    llm = MockLLMProvider(canned_response=canned)
    engine = LearningEngine(llm)
    engine.initialize()

    request = LearningPlanRequestDTO(
        profession="Fachinformatiker",
        school_subjects=["WIFI", "AE"],
        strengths=["Programmieren"],
        weaknesses=["Netzwerktechnik"],
        exam_date="2026-11-30"
    )

    plan = engine.generate_learning_plan(request)
    assert plan is not None
    assert plan.profession == "Fachinformatiker"
    assert len(plan.items) == 1

    analysis = engine.analyze_weaknesses(request)
    assert "Netzwerktechnik" in analysis.identified_weaknesses
    assert len(analysis.recommended_focus_areas) == 1

    update = LearningProgressUpdateDTO(
        plan_id=plan.plan_id,
        topic="TCP/IP",
        status="completed"
    )
    progress = engine.update_progress(update)
    assert progress.completed_items == 1
    assert progress.completion_rate == 1.0

    fetched = engine.get_learning_plan(plan.plan_id)
    assert fetched is not None
    assert len(engine.list_learning_plans()) == 1

    with pytest.raises(NotFoundError):
        engine.update_progress(LearningProgressUpdateDTO(plan_id="invalid", topic="TCP/IP", status="completed"))

def test_api_learning_endpoints(monkeypatch):
    monkeypatch.setenv("AZUBI_LLM_PROVIDER", "mock")

    response = client.post(
        "/api/v1/learning/plans/generate",
        json={
            "profession": "Fachinformatiker",
            "school_subjects": ["Anwendungsentwicklung"],
            "strengths": ["Logik"],
            "weaknesses": ["Datenbanken"],
            "exam_date": "2026-12-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "plan_id" in data
    plan_id = data["plan_id"]

    resp_get = client.get(f"/api/v1/learning/plans/{plan_id}")
    assert resp_get.status_code == 200

    resp_analyze = client.post(
        "/api/v1/learning/analyze",
        json={
            "profession": "Fachinformatiker",
            "weaknesses": ["Datenbanken"]
        }
    )
    assert resp_analyze.status_code == 200
    assert "identified_weaknesses" in resp_analyze.json()

    resp_progress = client.post(
        "/api/v1/learning/progress",
        json={
            "plan_id": plan_id,
            "topic": "Datenbanken",
            "status": "completed"
        }
    )
    assert resp_progress.status_code == 200
    assert "completion_rate" in resp_progress.json()