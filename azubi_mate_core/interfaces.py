# azubi_mate_core/interfaces.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar
from .dto import (
    KnowledgeItemDTO,
    KnowledgeSearchQueryDTO,
    ResearchQueryDTO,
    ResearchResultDTO,
    LLMRequestDTO,
    LLMResponseDTO,
    ReportRequestDTO,
    ReportDTO,
    DocumentExportRequestDTO,
    DocumentExportResultDTO,
    ExamQuestionDTO,
    ExamGenerateRequestDTO,
    ExamSubmissionDTO,
    ExamEvaluationDTO,
    ExamSessionDTO,
    ExamProgressDTO,
    LearningPlanRequestDTO,
    LearningPlanDTO,
    WeaknessAnalysisDTO,
    LearningProgressUpdateDTO,
    LearningProgressDTO,
)

class BaseEngine(ABC):
    """Base interface for all engines in Azubi-Mate."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initializes the engine."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Returns the current status of the engine."""
        pass

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    """Base interface for repository pattern data access."""
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Adds an entity to the persistence store."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Retrieves an entity by its unique identifier."""
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        """Retrieves all entities from the persistence store."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Deletes an entity by its unique identifier."""
        pass

class KnowledgeEngineInterface(BaseEngine, ABC):
    """Interface for the Knowledge Engine."""

    @abstractmethod
    def add_knowledge(self, item: KnowledgeItemDTO) -> KnowledgeItemDTO:
        """Adds or updates a knowledge item."""
        pass

    @abstractmethod
    def get_knowledge(self, item_id: str) -> Optional[KnowledgeItemDTO]:
        """Retrieves a knowledge item by ID."""
        pass

    @abstractmethod
    def search_knowledge(self, query: KnowledgeSearchQueryDTO) -> List[KnowledgeItemDTO]:
        """Searches knowledge items based on query and category."""
        pass

    @abstractmethod
    def list_knowledge(self) -> List[KnowledgeItemDTO]:
        """Lists all knowledge items."""
        pass

class ResearchEngineInterface(BaseEngine, ABC):
    """Interface for the Research Engine."""

    @abstractmethod
    def research(self, query: ResearchQueryDTO) -> ResearchResultDTO:
        """Conducts research across local knowledge base and external sources if needed."""
        pass

class ReportEngineInterface(BaseEngine, ABC):
    """Interface for the Report Engine."""

    @abstractmethod
    def generate_report(self, request: ReportRequestDTO) -> ReportDTO:
        """Generates an IHK-compliant training report from bullet points and analysis."""
        pass

    @abstractmethod
    def confirm_report(self, report_id: str) -> ReportDTO:
        """Confirms a report draft."""
        pass

    @abstractmethod
    def get_report(self, report_id: str) -> Optional[ReportDTO]:
        """Retrieves a report by ID."""
        pass

    @abstractmethod
    def list_reports(self) -> List[ReportDTO]:
        """Lists all reports."""
        pass

class DocumentEngineInterface(BaseEngine, ABC):
    """Interface for the Document Engine."""

    @abstractmethod
    def export_document(self, request: DocumentExportRequestDTO) -> DocumentExportResultDTO:
        """Exports a document in the requested format (PDF, Word, etc.)."""
        pass

class ExamEngineInterface(BaseEngine, ABC):
    """Interface for the Exam Engine."""

    @abstractmethod
    def generate_exam(self, request: ExamGenerateRequestDTO) -> ExamSessionDTO:
        """Generates exam questions, flashcards, or a simulation."""
        pass

    @abstractmethod
    def submit_answer(self, session_id: str, submission: ExamSubmissionDTO) -> ExamEvaluationDTO:
        """Submits and evaluates an answer for a question in a session."""
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[ExamSessionDTO]:
        """Retrieves an exam session by ID."""
        pass

    @abstractmethod
    def get_progress(self) -> ExamProgressDTO:
        """Retrieves learning and exam progress statistics."""
        pass

class LearningEngineInterface(BaseEngine, ABC):
    """Interface for the Learning Engine."""

    @abstractmethod
    def generate_learning_plan(self, request: LearningPlanRequestDTO) -> LearningPlanDTO:
        """Generates an individual learning plan."""
        pass

    @abstractmethod
    def analyze_weaknesses(self, request: LearningPlanRequestDTO) -> WeaknessAnalysisDTO:
        """Analyzes weaknesses and recommends focus areas."""
        pass

    @abstractmethod
    def update_progress(self, update: LearningProgressUpdateDTO) -> LearningProgressDTO:
        """Updates progress of a learning plan item."""
        pass

    @abstractmethod
    def get_learning_plan(self, plan_id: str) -> Optional[LearningPlanDTO]:
        """Retrieves a learning plan by ID."""
        pass

    @abstractmethod
    def list_learning_plans(self) -> List[LearningPlanDTO]:
        """Lists all learning plans."""
        pass

class LLMProvider(ABC):
    """Interface for LLM providers (Ollama, OpenAI, Gemini, etc.)."""

    @abstractmethod
    def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        """Generates a response from the LLM provider."""
        pass