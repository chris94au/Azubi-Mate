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
    ExamGenerateRequestDTO,
    ExamSessionDTO,
    ExamSubmissionDTO,
    ExamEvaluationDTO,
    ExamProgressDTO,
    LearningPlanRequestDTO,
    LearningPlanDTO,
    WeaknessAnalysisDTO,
    LearningProgressUpdateDTO,
    LearningProgressDTO,
    ReportEngineInterface,
    DocumentEngineInterface,
    ExamEngineInterface,
    LearningEngineInterface,
)
from backend.dependencies import get_report_engine, get_document_engine, get_exam_engine, get_learning_engine

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

@api_router.post("/exams/generate", response_model=ExamSessionDTO)
def generate_exam(
    request: ExamGenerateRequestDTO,
    exam_engine: ExamEngineInterface = Depends(get_exam_engine)
) -> ExamSessionDTO:
    """Generates an exam session (flashcards, multiple choice, open questions, simulation)."""
    return exam_engine.generate_exam(request)

@api_router.post("/exams/{session_id}/submit", response_model=ExamEvaluationDTO)
def submit_exam_answer(
    session_id: str,
    submission: ExamSubmissionDTO,
    exam_engine: ExamEngineInterface = Depends(get_exam_engine)
) -> ExamEvaluationDTO:
    """Submits and evaluates an answer for an exam session."""
    session = exam_engine.get_session(session_id)
    if not session:
        raise NotFoundError(f"Exam session with id {session_id} not found.")
    return exam_engine.submit_answer(session_id, submission)

@api_router.get("/exams/{session_id}", response_model=ExamSessionDTO)
def get_exam_session(
    session_id: str,
    exam_engine: ExamEngineInterface = Depends(get_exam_engine)
) -> ExamSessionDTO:
    """Retrieves an exam session by ID."""
    session = exam_engine.get_session(session_id)
    if not session:
        raise NotFoundError(f"Exam session with id {session_id} not found.")
    return session

@api_router.get("/exams/progress", response_model=ExamProgressDTO)
def get_exam_progress(
    exam_engine: ExamEngineInterface = Depends(get_exam_engine)
) -> ExamProgressDTO:
    """Retrieves exam and learning progress."""
    return exam_engine.get_progress()

@api_router.post("/learning/plans/generate", response_model=LearningPlanDTO)
def generate_learning_plan(
    request: LearningPlanRequestDTO,
    learning_engine: LearningEngineInterface = Depends(get_learning_engine)
) -> LearningPlanDTO:
    """Generates an individual learning plan."""
    return learning_engine.generate_learning_plan(request)

@api_router.post("/learning/analyze", response_model=WeaknessAnalysisDTO)
def analyze_weaknesses(
    request: LearningPlanRequestDTO,
    learning_engine: LearningEngineInterface = Depends(get_learning_engine)
) -> WeaknessAnalysisDTO:
    """Analyzes weaknesses and recommends focus areas."""
    return learning_engine.analyze_weaknesses(request)

@api_router.post("/learning/progress", response_model=LearningProgressDTO)
def update_learning_progress(
    update: LearningProgressUpdateDTO,
    learning_engine: LearningEngineInterface = Depends(get_learning_engine)
) -> LearningProgressDTO:
    """Updates progress of a learning plan item."""
    return learning_engine.update_progress(update)

@api_router.get("/learning/plans/{plan_id}", response_model=LearningPlanDTO)
def get_learning_plan(
    plan_id: str,
    learning_engine: LearningEngineInterface = Depends(get_learning_engine)
) -> LearningPlanDTO:
    """Retrieves a learning plan by ID."""
    plan = learning_engine.get_learning_plan(plan_id)
    if not plan:
        raise NotFoundError(f"Learning plan with id {plan_id} not found.")
    return plan

@api_router.get("/learning/plans", response_model=list[LearningPlanDTO])
def list_learning_plans(
    learning_engine: LearningEngineInterface = Depends(get_learning_engine)
) -> list[LearningPlanDTO]:
    """Lists all learning plans."""
    return learning_engine.list_learning_plans()