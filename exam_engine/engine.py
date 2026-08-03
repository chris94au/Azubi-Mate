# exam_engine/engine.py
import uuid
from typing import Any, Dict, List, Optional
from azubi_mate_core import (
    ExamEngineInterface,
    ExamGenerateRequestDTO,
    ExamSessionDTO,
    ExamQuestionDTO,
    ExamSubmissionDTO,
    ExamEvaluationDTO,
    ExamProgressDTO,
    LLMProvider,
    LLMRequestDTO,
    ValidationException,
    NotFoundError,
    logger,
)

class ExamEngine(ExamEngineInterface):
    """Implementation of the Exam Engine for training, flashcards, multiple choice, open questions, and simulations."""

    def __init__(self, llm_provider: LLMProvider) -> None:
        self.llm_provider = llm_provider
        self._sessions: Dict[str, ExamSessionDTO] = {}
        self._progress_history: List[dict] = []
        self._initialized = False

    def initialize(self) -> None:
        logger.info("Initializing Exam Engine...")
        self._initialized = True
        logger.info("Exam Engine initialized successfully.")

    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": "ExamEngine",
            "status": "active" if self._initialized else "inactive",
            "sessions_count": len(self._sessions),
        }

    def generate_exam(self, request: ExamGenerateRequestDTO) -> ExamSessionDTO:
        logger.info(f"Generating exam session for topic '{request.topic}' of type '{request.question_type}'...")

        q_type = request.question_type or "multiple_choice"
        count = request.count or 5
        topic = request.topic or "Allgemeines Ausbildungswissen"

        prompt = (
            f"Erstelle genau {count} Prüfungsfragen zum Thema '{topic}' (Kategorie: {request.category or 'Allgemein'}) "
            f"des Typs '{q_type}'.\n"
            "Gib jede Frage in folgendem exakten Textformat aus:\n"
            "FRAGE:\n"
            "Typ: [multiple_choice | flashcard | open]\n"
            "Fragetext: [Text der Frage]\n"
            "Optionen: [Option A, Option B, Option C, Option D (nur bei multiple_choice)]\n"
            "Antwort: [Richtige Antwort oder Stichpunkte]\n"
            "Erklärung: [Kurze Erklärung]\n"
            "---"
        )

        llm_request = LLMRequestDTO(
            prompt=prompt,
            system_prompt="Du bist ein professioneller IHK-Prüfungsexperte, der realistische Prüfungsfragen und Karteikarten erstellt.",
            temperature=0.4,
        )

        questions: List[ExamQuestionDTO] = []
        try:
            llm_response = self.llm_provider.generate(llm_request)
            text = llm_response.text
            
            blocks = text.split("---")
            for block in blocks:
                if "Fragetext:" in block:
                    lines = block.strip().split("\n")
                    f_type = q_type
                    f_text = ""
                    options = []
                    correct = "Beispielantwort"
                    explanation = "Erklärung zum Thema."

                    for line in lines:
                        l_stripped = line.strip()
                        if l_stripped.startswith("Typ:"):
                            ft = l_stripped.replace("Typ:", "").strip().lower()
                            if ft in ["multiple_choice", "flashcard", "open"]:
                                f_type = ft
                        elif l_stripped.startswith("Fragetext:"):
                            f_text = l_stripped.replace("Fragetext:", "").strip()
                        elif l_stripped.startswith("Optionen:"):
                            opt_str = l_stripped.replace("Optionen:", "").strip()
                            options = [o.strip() for o in opt_str.split(",") if o.strip()]
                        elif l_stripped.startswith("Antwort:"):
                            correct = l_stripped.replace("Antwort:", "").strip()
                        elif l_stripped.startswith("Erklärung:"):
                            explanation = l_stripped.replace("Erklärung:", "").strip()

                    if f_text:
                        questions.append(
                            ExamQuestionDTO(
                                id=str(uuid.uuid4()),
                                question_type=f_type,
                                question_text=f_text,
                                options=options,
                                correct_answer=correct,
                                explanation=explanation,
                            )
                        )
        except Exception as e:
            logger.warning(f"LLM generation failed for exam questions, falling back to default questions: {e}")

        if not questions:
            for i in range(count):
                questions.append(
                    ExamQuestionDTO(
                        id=str(uuid.uuid4()),
                        question_type=q_type if q_type in ["multiple_choice", "flashcard", "open"] else "multiple_choice",
                        question_text=f"Beispielfrage {i+1} zu {topic}",
                        options=["Option A", "Option B", "Option C", "Option D"] if (q_type == "multiple_choice") else [],
                        correct_answer="Option A" if (q_type == "multiple_choice") else "Musterantwort",
                        explanation="Dies ist eine generierte Fallback-Erklärung.",
                    )
                )

        session_id = str(uuid.uuid4())
        session = ExamSessionDTO(
            session_id=session_id,
            title=f"Prüfungstraining: {topic}",
            questions=questions,
            answers={},
            evaluations=[],
            score=0.0,
            completed=False,
        )

        self._sessions[session_id] = session
        logger.info(f"Exam session {session_id} created with {len(questions)} questions.")
        return session

    def submit_answer(self, session_id: str, submission: ExamSubmissionDTO) -> ExamEvaluationDTO:
        if session_id not in self._sessions:
            raise NotFoundError(f"Exam session with id {session_id} not found.")

        session = self._sessions[session_id]
        question = next((q for q in session.questions if q.id == submission.question_id), None)
        if not question:
            raise NotFoundError(f"Question with id {submission.question_id} not found in session.")

        logger.info(f"Evaluating answer for question {submission.question_id} in session {session_id}...")

        is_correct = False
        score = 0.0
        feedback = ""

        if question.question_type == "multiple_choice":
            if question.correct_answer and submission.answer.strip().lower() == question.correct_answer.strip().lower():
                is_correct = True
                score = 1.0
                feedback = "Richtig! " + (question.explanation or "")
            else:
                is_correct = False
                score = 0.0
                feedback = f"Falsch. Richtige Antwort wäre: {question.correct_answer}. {question.explanation or ''}"
        else:
            if question.correct_answer and (submission.answer.strip().lower() in question.correct_answer.strip().lower() or len(submission.answer) > 5):
                is_correct = True
                score = 1.0
                feedback = "Gute Antwort! " + (question.explanation or "")
            else:
                is_correct = True
                score = 0.75
                feedback = "Akzeptiert. Musterantwort: " + (question.correct_answer or "")

        evaluation = ExamEvaluationDTO(
            question_id=question.id,
            correct=is_correct,
            score=score,
            feedback=feedback,
            correct_answer=question.correct_answer,
        )

        session.answers[question.id] = submission.answer
        session.evaluations.append(evaluation)

        if len(session.evaluations) == len(session.questions):
            session.completed = True
            total_score = sum(ev.score for ev in session.evaluations)
            session.score = total_score / len(session.questions)
            
            self._progress_history.append({
                "session_id": session.session_id,
                "title": session.title,
                "score": session.score,
                "total_questions": len(session.questions),
            })

        self._sessions[session_id] = session
        return evaluation

    def get_session(self, session_id: str) -> Optional[ExamSessionDTO]:
        return self._sessions.get(session_id)

    def get_progress(self) -> ExamProgressDTO:
        total_sessions = len(self._progress_history)
        total_answered = sum(h["total_questions"] for h in self._progress_history)
        correct_answers = sum(1 for s in self._sessions.values() for ev in s.evaluations if ev.correct)
        avg_score = sum(h["score"] for h in self._progress_history) / total_sessions if total_sessions > 0 else 0.0

        return ExamProgressDTO(
            total_sessions=total_sessions,
            total_answered=total_answered,
            correct_answers=correct_answers,
            average_score=avg_score,
            history=self._progress_history,
        )