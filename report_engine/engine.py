# report_engine/engine.py
import uuid
from typing import Any, Dict, List, Optional
from azubi_mate_core import (
    ReportEngineInterface,
    ReportRequestDTO,
    ReportDTO,
    LLMProvider,
    LLMRequestDTO,
    ValidationException,
    NotFoundError,
    logger,
)

class ReportEngine(ReportEngineInterface):
    """Implementation of the Report Engine for creating IHK-compliant training reports."""

    def __init__(self, llm_provider: LLMProvider) -> None:
        self.llm_provider = llm_provider
        self._reports: Dict[str, ReportDTO] = {}
        self._initialized = False

    def initialize(self) -> None:
        logger.info("Initializing Report Engine...")
        self._initialized = True
        logger.info("Report Engine initialized successfully.")

    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": "ReportEngine",
            "status": "active" if self._initialized else "inactive",
            "reports_count": len(self._reports),
        }

    def generate_report(self, request: ReportRequestDTO) -> ReportDTO:
        if not request.bullet_points:
            raise ValidationException("Bullet points are required to generate a report.")

        logger.info(f"Generating {request.report_type} report from {len(request.bullet_points)} bullet points...")

        prompt = (
            f"Analysiere die folgenden Stichpunkte für einen IHK-konformen {request.report_type}:\n"
            + "\n".join([f"- {bp}" for bp in request.bullet_points]) + "\n\n"
            "Erstelle daraus strukturierte Inhalte in folgendem Format:\n"
            "Titel: [Titel des Berichts]\n"
            "Tätigkeiten:\n- [Tätigkeit 1]\n- [Tätigkeit 2]\n"
            "Lerninhalte:\n- [Lerninhalt 1]\n- [Lerninhalt 2]\n"
            "Fachbegriffe:\n- [Begriff 1]\n- [Begriff 2]\n"
            "Zusammenfassung:\n[Zusammenfassung des Berichts]"
        )

        llm_request = LLMRequestDTO(
            prompt=prompt,
            system_prompt="Du bist ein professioneller Ausbildungsassistent, der IHK-konforme Ausbildungsnachweise erstellt.",
            temperature=0.3,
        )

        try:
            llm_response = self.llm_provider.generate(llm_request)
            text = llm_response.text
        except Exception as e:
            logger.warning(f"LLM generation failed for report, falling back to heuristic parsing: {e}")
            text = ""

        title = f"Ausbildungsnachweis ({request.report_type})"
        activities = list(request.bullet_points)
        learning_content = ["Allgemeine Unterweisung und praktische Durchführung"]
        technical_terms = ["Fachkompetenz", "Dokumentation"]
        summary = f"Bericht erstellt auf Basis von {len(request.bullet_points)} Stichpunkten."

        if text:
            try:
                lines = text.split("\n")
                current_section = None
                parsed_activities = []
                parsed_learning = []
                parsed_terms = []
                parsed_summary_lines = []

                for line in lines:
                    line_stripped = line.strip()
                    if line_stripped.startswith("Titel:"):
                        title = line_stripped.replace("Titel:", "").strip()
                    elif "Tätigkeiten" in line_stripped:
                        current_section = "activities"
                    elif "Lerninhalte" in line_stripped:
                        current_section = "learning"
                    elif "Fachbegriffe" in line_stripped:
                        current_section = "terms"
                    elif "Zusammenfassung" in line_stripped:
                        current_section = "summary"
                    elif line_stripped.startswith("-") or line_stripped.startswith("*"):
                        item = line_stripped.lstrip("-* ").strip()
                        if current_section == "activities":
                            parsed_activities.append(item)
                        elif current_section == "learning":
                            parsed_learning.append(item)
                        elif current_section == "terms":
                            parsed_terms.append(item)
                    elif current_section == "summary" and line_stripped:
                        parsed_summary_lines.append(line_stripped)

                if parsed_activities:
                    activities = parsed_activities
                if parsed_learning:
                    learning_content = parsed_learning
                if parsed_terms:
                    technical_terms = parsed_terms
                if parsed_summary_lines:
                    summary = " ".join(parsed_summary_lines)
            except Exception as parse_err:
                logger.error(f"Failed to parse LLM response for report: {parse_err}")

        report_id = str(uuid.uuid4())
        report = ReportDTO(
            id=report_id,
            report_type=request.report_type,
            title=title,
            activities=activities,
            learning_content=learning_content,
            technical_terms=technical_terms,
            summary=summary,
            date=request.date,
            week_number=request.week_number,
            month=request.month,
            year=request.year,
            status="draft",
        )

        self._reports[report_id] = report
        logger.info(f"Report generated successfully with id {report_id}")
        return report

    def confirm_report(self, report_id: str) -> ReportDTO:
        if report_id not in self._reports:
            raise NotFoundError(f"Report with id {report_id} not found.")
        report = self._reports[report_id]
        updated = report.model_copy(update={"status": "confirmed"})
        self._reports[report_id] = updated
        logger.info(f"Report {report_id} confirmed.")
        return updated

    def get_report(self, report_id: str) -> Optional[ReportDTO]:
        return self._reports.get(report_id)

    def list_reports(self) -> List[ReportDTO]:
        return list(self._reports.values())