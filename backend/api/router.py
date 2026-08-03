# backend/api/router.py
from fastapi import APIRouter, Depends
from azubi_mate_core import (
    config, 
    NotFoundError, 
    ValidationException, 
    AzubiMateException,
    ReportRequestDTO,
    ReportDTO,
    DocumentExportRequestDTO,
    DocumentExportResultDTO,
    ReportEngineInterface,
    DocumentEngineInterface,
)
from backend.dependencies import get_report_engine, get_document_engine

api_router = APIRouter(prefix="/api/v1")

@api_router.get("/status")
def api_status() -> dict[str, str]:
    """API status endpoint."""
    return {
        "status": "active",
        "app": config.app_name,
        "version": config.version,
    }

@api_router.get("/test-not-found")
def trigger_not_found() -> None:
    raise NotFoundError("Resource not found")

@api_router.get("/test-validation")
def trigger_validation() -> None:
    raise ValidationException("Invalid input data")

@api_router.get("/test-core-error")
def trigger_core_error() -> None:
    raise AzubiMateException("Core general error")

@api_router.post("/reports/generate", response_model=ReportDTO)
def generate_report(
    request: ReportRequestDTO,
    report_engine: ReportEngineInterface = Depends(get_report_engine)
) -> ReportDTO:
    """Generates an IHK-compliant training report."""
    return report_engine.generate_report(request)

@api_router.post("/reports/{report_id}/confirm", response_model=ReportDTO)
def confirm_report(
    report_id: str,
    report_engine: ReportEngineInterface = Depends(get_report_engine)
) -> ReportDTO:
    """Confirms a report draft."""
    report = report_engine.get_report(report_id)
    if not report:
        raise NotFoundError(f"Report with id {report_id} not found.")
    return report_engine.confirm_report(report_id)

@api_router.get("/reports/{report_id}", response_model=ReportDTO)
def get_report(
    report_id: str,
    report_engine: ReportEngineInterface = Depends(get_report_engine)
) -> ReportDTO:
    """Retrieves a report by ID."""
    report = report_engine.get_report(report_id)
    if not report:
        raise NotFoundError(f"Report with id {report_id} not found.")
    return report
    
@api_router.get("/reports", response_model=list[ReportDTO])
def list_reports(
    report_engine: ReportEngineInterface = Depends(get_report_engine)
) -> list[ReportDTO]:
    """Lists all reports."""
    return report_engine.list_reports()

@api_router.post("/documents/export", response_model=DocumentExportResultDTO)
def export_document(
    request: DocumentExportRequestDTO,
    doc_engine: DocumentEngineInterface = Depends(get_document_engine)
) -> DocumentExportResultDTO:
    """Exports a document (e.g., report PDF/Word)."""
    return doc_engine.export_document(request)