# tests/test_phase_7.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from azubi_mate_core import (
    ReportRequestDTO,
    ReportDTO,
    DocumentExportRequestDTO,
    ValidationException,
    NotFoundError,
)
from backend.ai import MockLLMProvider
from report_engine import ReportEngine
from document_engine import DocumentEngine

client = TestClient(app)

def test_report_engine_initialization():
    llm = MockLLMProvider(canned_response="Titel: Tagesbericht Test\nTätigkeiten:\n- Arbeit 1\nLerninhalte:\n- Lernen 1\nFachbegriffe:\n- Python\nZusammenfassung:\nGuter Tag.")
    engine = ReportEngine(llm)
    engine.initialize()
    status = engine.get_status()
    assert status["engine"] == "ReportEngine"
    assert status["status"] == "active"
    assert status["reports_count"] == 0

def test_generate_and_confirm_report():
    canned = (
        "Titel: Wochenbericht 5\n"
        "Tätigkeiten:\n"
        "- API entwickelt\n"
        "- Tests geschrieben\n"
        "Lerninhalte:\n"
        "- FastAPI Routing\n"
        "Fachbegriffe:\n"
        "- REST\n"
        "Zusammenfassung:\n"
        "Erfolgreiche Woche mit Backend-Fokus."
    )
    llm = MockLLMProvider(canned_response=canned)
    engine = ReportEngine(llm)
    engine.initialize()

    request = ReportRequestDTO(
        report_type="wochenbericht",
        bullet_points=["API entwickelt", "Tests geschrieben"],
        week_number=5,
        year=2026,
    )

    report = engine.generate_report(request)
    assert report is not None
    assert report.report_type == "wochenbericht"
    assert report.title == "Wochenbericht 5"
    assert len(report.activities) == 2
    assert report.status == "draft"
    assert engine.get_report(report.id) == report
    assert len(engine.list_reports()) == 1

    confirmed = engine.confirm_report(report.id)
    assert confirmed.status == "confirmed"

    with pytest.raises(NotFoundError):
        engine.confirm_report("non-existent-id")

def test_report_validation_error():
    llm = MockLLMProvider()
    engine = ReportEngine(llm)
    engine.initialize()

    with pytest.raises(ValidationException):
        engine.generate_report(ReportRequestDTO(report_type="tagesbericht", bullet_points=[]))

def test_document_engine_export(tmp_path):
    output_dir = tmp_path / "exports"
    doc_engine = DocumentEngine(output_dir=str(output_dir))
    doc_engine.initialize()

    status = doc_engine.get_status()
    assert status["engine"] == "DocumentEngine"
    assert status["status"] == "active"

    export_req = DocumentExportRequestDTO(
        title="Ausbildungsnachweis_Test",
        content="Inhalt des Ausbildungsnachweises...",
        format="pdf",
        metadata={"author": "Azubi"}
    )

    result = doc_engine.export_document(export_req)
    assert result.success is True
    assert result.format == "pdf"
    assert result.file_path is not None

    with pytest.raises(ValidationException):
        doc_engine.export_document(DocumentExportRequestDTO(title="", content="", format="pdf"))

def test_api_reports_and_documents(monkeypatch):
    monkeypatch.setenv("AZUBI_LLM_PROVIDER", "mock")
    
    response = client.post(
        "/api/v1/reports/generate",
        json={
            "report_type": "tagesbericht",
            "bullet_points": ["Bugfix durchgeführt", "Code Review"],
            "date": "2026-08-03"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["report_type"] == "tagesbericht"
    assert data["status"] == "draft"
    report_id = data["id"]

    resp_confirm = client.post(f"/api/v1/reports/{report_id}/confirm")
    assert resp_confirm.status_code == 200
    assert resp_confirm.json()["status"] == "confirmed"

    resp_get = client.get(f"/api/v1/reports/{report_id}")
    assert resp_get.status_code == 200

    resp_list = client.get("/api/v1/reports")
    assert resp_list.status_code == 200
    assert len(resp_list.json()) >= 1

    resp_export = client.post(
        "/api/v1/documents/export",
        json={
            "title": "API_Export_Test",
            "content": "Export content via API",
            "format": "pdf"
        }
    )
    assert resp_export.status_code == 200
    assert resp_export.json()["success"] is True