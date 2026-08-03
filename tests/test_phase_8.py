# tests/test_phase_8.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from azubi_mate_core import (
    ExamGenerateRequestDTO,
    ExamSessionDTO,
    ExamSubmissionDTO,
    ExamEvaluationDTO,
    ExamProgressDTO,
    NotFoundError,
)
from backend.ai import MockLLMProvider
from exam_engine import ExamEngine

client = TestClient(app)

def test_exam_engine_initialization():
    llm = MockLLMProvider(canned_response=(
        "FRAGE:\n"
        "Typ: multiple_choice\n"
        "Fragetext: Was ist Python?\n"
        "Optionen: Programmiersprache, Schlangengattung, Betriebssystem, Datenbank\n"
        "Antwort: Programmiersprache\n"
        "Erklärung: Python ist eine interpretierte Programmiersprache.\n"
        "---"
    ))
    engine = ExamEngine(llm)
    engine.initialize()
    status = engine.get_status()
    assert status["engine"] == "ExamEngine"
    assert status["status"] == "active"
    assert status["sessions_count"] == 0

def test_generate_and_submit_exam():
    canned = (
        "FRAGE:\n"
        "Typ: multiple_choice\n"
        "Fragetext: Was ist HTTP?\n"
        "Optionen: Protokoll, Datenbank, Betriebssystem, Editor\n"
        "Antwort: Protokoll\n"
        "Erklärung: HTTP ist ein Übertragungsprotokoll.\n"
        "---"
    )
    llm = MockLLMProvider(canned_response=canned)
    engine = ExamEngine(llm)
    engine.initialize()

    request = ExamGenerateRequestDTO(
        topic="Netzwerke",
        question_type="multiple_choice",
        count=1,
    )

    session = engine.generate_exam(request)
    assert session is not None
    assert len(session.questions) == 1
    assert session.completed is False

    q_id = session.questions[0].id
    
    eval_resp = engine.submit_answer(session.session_id, ExamSubmissionDTO(question_id=q_id, answer="Protokoll"))
    assert eval_resp.correct is True
    assert eval_resp.score == 1.0

    updated_session = engine.get_session(session.session_id)
    assert updated_session.completed is True
    assert updated_session.score == 1.0

    progress = engine.get_progress()
    assert progress.total_sessions == 1
    assert progress.total_answered == 1
    assert progress.correct_answers == 1

    with pytest.raises(NotFoundError):
        engine.submit_answer("non-existent-session", ExamSubmissionDTO(question_id="1", answer="Test"))

def test_api_exam_endpoints(monkeypatch):
    monkeypatch.setenv("AZUBI_LLM_PROVIDER", "mock")

    response = client.post(
        "/api/v1/exams/generate",
        json={
            "topic": "Python",
            "question_type": "flashcard",
            "count": 2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert len(data["questions"]) > 0
    session_id = data["session_id"]
    q_id = data["questions"][0]["id"]

    resp_get = client.get(f"/api/v1/exams/{session_id}")
    assert resp_get.status_code == 200

    resp_submit = client.post(
        f"/api/v1/exams/{session_id}/submit",
        json={
            "question_id": q_id,
            "answer": "Test Antwort"
        }
    )
    assert resp_submit.status_code == 200
    assert "score" in resp_submit.json()

    resp_progress = client.get("/api/v1/exams/progress")
    assert resp_progress.status_code == 200
    assert "total_sessions" in resp_progress.json()