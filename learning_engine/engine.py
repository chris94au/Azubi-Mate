# learning_engine/engine.py
import uuid
from typing import Any, Dict, List, Optional
from azubi_mate_core import (
    LearningEngineInterface,
    LearningPlanRequestDTO,
    LearningPlanDTO,
    LearningPlanItemDTO,
    WeaknessAnalysisDTO,
    LearningProgressUpdateDTO,
    LearningProgressDTO,
    LLMProvider,
    LLMRequestDTO,
    ValidationException,
    NotFoundError,
    logger,
)

class LearningEngine(LearningEngineInterface):
    """Implementation of the Learning Engine for individual learning plans and weakness analysis."""

    def __init__(self, llm_provider: LLMProvider) -> None:
        self.llm_provider = llm_provider
        self._plans: Dict[str, LearningPlanDTO] = {}
        self._progress: Dict[str, Dict[str, str]] = {}
        self._initialized = False

    def initialize(self) -> None:
        logger.info("Initializing Learning Engine...")
        self._initialized = True
        logger.info("Learning Engine initialized successfully.")

    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": "LearningEngine",
            "status": "active" if self._initialized else "inactive",
            "plans_count": len(self._plans),
        }

    def generate_learning_plan(self, request: LearningPlanRequestDTO) -> LearningPlanDTO:
        logger.info(f"Generating learning plan for profession '{request.profession}'...")

        profession = request.profession or "Ausbildung"
        subjects = request.school_subjects or ["Allgemeine Fächer"]
        strengths = request.strengths or []
        weaknesses = request.weaknesses or ["Grundlagen"]
        exam_date = request.exam_date or "N/A"

        prompt = (
            f"Erstelle einen individuellen Lernplan für den Ausbildungsberuf '{profession}'.\n"
            f"Schulfächer: {', '.join(subjects)}\n"
            f"Stärken: {', '.join(strengths)}\n"
            f"Schwächen: {', '.join(weaknesses)}\n"
            f"Prüfungstermin: {exam_date}\n\n"
            "Gib den Lernplan in folgendem exakten Format aus:\n"
            "Titel: [Titel des Lernplans]\n"
            "Zusammenfassung: [Zusammenfassung des Lernplans]\n"
            "THEMA:\n"
            "Name: [Themenname]\n"
            "Priorität: [high | medium | low]\n"
            "Aktionen: [Aktion 1, Aktion 2, Aktion 3]\n"
            "---"
        )

        llm_request = LLMRequestDTO(
            prompt=prompt,
            system_prompt="Du bist ein erfahrener Ausbildungsleiter und Prüfungscoach, der strukturierte, individuelle Lernpläne erstellt.",
            temperature=0.4,
        )

        items: List[LearningPlanItemDTO] = []
        title = f"Lernplan für {profession}"
        summary = f"Individueller Lernplan fokussiert auf Schwächen: {', '.join(weaknesses)}."

        try:
            llm_response = self.llm_provider.generate(llm_request)
            text = llm_response.text
            blocks = text.split("---")
            
            parsed_items = []
            for block in blocks:
                if "Name:" in block:
                    lines = block.strip().split("\n")
                    t_name = ""
                    t_prio = "medium"
                    t_actions = ["Lernkarten bearbeiten", "Übungsaufgaben lösen"]

                    for line in lines:
                        l_stripped = line.strip()
                        if l_stripped.startswith("Titel:") and not title.startswith("Lernplan für"):
                            title = l_stripped.replace("Titel:", "").strip()
                        elif l_stripped.startswith("Zusammenfassung:"):
                            summary = l_stripped.replace("Zusammenfassung:", "").strip()
                        elif l_stripped.startswith("Name:"):
                            t_name = l_stripped.replace("Name:", "").strip()
                        elif l_stripped.startswith("Priorität:"):
                            p = l_stripped.replace("Priorität:", "").strip().lower()
                            if p in ["high", "medium", "low"]:
                                t_prio = p
                        elif l_stripped.startswith("Aktionen:"):
                            act_str = l_stripped.replace("Aktionen:", "").strip()
                            t_actions = [a.strip() for a in act_str.split(",") if a.strip()]

                    if t_name:
                        parsed_items.append(
                            LearningPlanItemDTO(
                                topic=t_name,
                                priority=t_prio,
                                suggested_actions=t_actions,
                                status="open",
                            )
                        )
            if parsed_items:
                items = parsed_items
        except Exception as e:
            logger.warning(f"LLM generation failed for learning plan, falling back to default plan: {e}")

        if not items:
            for w in weaknesses:
                items.append(
                    LearningPlanItemDTO(
                        topic=w,
                        priority="high",
                        suggested_actions=["Fachliteratur lesen", "Prüfungsfragen lösen"],
                        status="open",
                    )
                )
            for s in subjects[:2]:
                items.append(
                    LearningPlanItemDTO(
                        topic=s,
                        priority="medium",
                        suggested_actions=["Wiederholung", "Zusammenfassung schreiben"],
                        status="open",
                    )
                )

        plan_id = str(uuid.uuid4())
        plan = LearningPlanDTO(
            plan_id=plan_id,
            title=title,
            profession=profession,
            items=items,
            summary=summary,
        )

        self._plans[plan_id] = plan
        self._progress[plan_id] = {item.topic: item.status for item in items}
        logger.info(f"Learning plan {plan_id} created with {len(items)} items.")
        return plan

    def analyze_weaknesses(self, request: LearningPlanRequestDTO) -> WeaknessAnalysisDTO:
        logger.info("Analyzing weaknesses and recommending focus areas...")
        weaknesses = request.weaknesses or ["Allgemeine Grundlagen"]
        recommendations = [f"Intensives Training für: {w}" for w in weaknesses]
        notes = f"Analyse basierend auf {len(weaknesses)} angegebenen Schwächen für den Beruf {request.profession or 'Ausbildung'}."

        return WeaknessAnalysisDTO(
            identified_weaknesses=weaknesses,
            recommended_focus_areas=recommendations,
            analysis_notes=notes,
        )

    def update_progress(self, update: LearningProgressUpdateDTO) -> LearningProgressDTO:
        if update.plan_id not in self._plans:
            raise NotFoundError(f"Learning plan with id {update.plan_id} not found.")

        plan = self._plans[update.plan_id]
        topic_found = False
        updated_items = []

        for item in plan.items:
            if item.topic.lower() == update.topic.lower():
                topic_found = True
                updated_items.append(item.model_copy(update={"status": update.status}))
            else:
                updated_items.append(item)

        if not topic_found:
            raise NotFoundError(f"Topic '{update.topic}' not found in learning plan {update.plan_id}.")

        plan = plan.model_copy(update={"items": updated_items})
        self._plans[update.plan_id] = plan

        if update.plan_id not in self._progress:
            self._progress[update.plan_id] = {}
        self._progress[update.plan_id][update.topic] = update.status

        total_items = len(plan.items)
        completed_items = sum(1 for it in plan.items if it.status == "completed")
        completion_rate = completed_items / total_items if total_items > 0 else 0.0

        items_status = {it.topic: it.status for it in plan.items}

        return LearningProgressDTO(
            plan_id=update.plan_id,
            completed_items=completed_items,
            total_items=total_items,
            completion_rate=completion_rate,
            items_status=items_status,
        )

    def get_learning_plan(self, plan_id: str) -> Optional[LearningPlanDTO]:
        return self._plans.get(plan_id)

    def list_learning_plans(self) -> List[LearningPlanDTO]:
        return list(self._plans.values())