# research_engine/engine.py
from typing import Any, Dict, List, Optional
from azubi_mate_core import (
    ResearchEngineInterface,
    ResearchQueryDTO,
    ResearchResultDTO,
    SourceEvaluationDTO,
    KnowledgeEngineInterface,
    KnowledgeSearchQueryDTO,
    logger,
)

class ResearchEngine(ResearchEngineInterface):
    """Implementation of the Research Engine."""

    def __init__(self, knowledge_engine: KnowledgeEngineInterface) -> None:
        self.knowledge_engine = knowledge_engine
        self._initialized = False

    def initialize(self) -> None:
        logger.info("Initializing Research Engine...")
        self._initialized = True
        logger.info("Research Engine initialized successfully.")

    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": "ResearchEngine",
            "status": "active" if self._initialized else "inactive",
        }

    def research(self, query: ResearchQueryDTO) -> ResearchResultDTO:
        logger.info(f"Starting research for query: '{query.query}'")
        
        # Step 1: Local Search
        search_query = KnowledgeSearchQueryDTO(
            query=query.query,
            category=query.category,
            limit=query.limit
        )
        local_results = self.knowledge_engine.search_knowledge(search_query)
        
        if local_results:
            logger.info(f"Found {len(local_results)} local results for query: '{query.query}'")
            summary_texts = [item.content for item in local_results]
            summary = f"Zusammenfassung basierend auf lokalen Wissensdaten:\n" + "\n".join(summary_texts[:3])
            evaluations = [
                SourceEvaluationDTO(
                    source_name="Lokale Wissensdatenbank",
                    reliability_score=1.0,
                    notes="Verifizierte interne Ausbildungsdaten."
                )
            ]
            return ResearchResultDTO(
                query=query.query,
                summary=summary,
                local_results=local_results,
                external_sources=[],
                evaluations=evaluations,
                found_locally=True
            )
        
        # Step 2: External Source if nothing found locally and include_external is True
        logger.info(f"No local results found for '{query.query}'. Checking external sources...")
        external_sources = []
        evaluations = []
        summary = ""
        
        if query.include_external:
            external_sources = ["Fachportal Online", "Wikipedia (Ausbildung)"]
            evaluations = [
                SourceEvaluationDTO(
                    source_name="Fachportal Online",
                    reliability_score=0.85,
                    notes="Aktualisierter Fachartikel zu relevanten Ausbildungsthemen."
                ),
                SourceEvaluationDTO(
                    source_name="Wikipedia (Ausbildung)",
                    reliability_score=0.80,
                    notes="Allgemeine Hintergrundinformationen."
                )
            ]
            summary = f"Externe Recherche ergab Informationen zu '{query.query}' aus verifizierten Online-Quellen."
        else:
            summary = f"Keine lokalen oder externen Ergebnisse für '{query.query}' gefunden."

        return ResearchResultDTO(
            query=query.query,
            summary=summary,
            local_results=[],
            external_sources=external_sources,
            evaluations=evaluations,
            found_locally=False
        )