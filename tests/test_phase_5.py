# tests/test_phase_5.py
import pytest
from azubi_mate_core import (
    ResearchQueryDTO,
    KnowledgeItemDTO,
    KnowledgeSearchQueryDTO,
    KnowledgeEngineInterface,
)
from research_engine import ResearchEngine

class MockKnowledgeEngine(KnowledgeEngineInterface):
    def __init__(self, return_items=None):
        self.return_items = return_items or []
        self.initialized = False

    def initialize(self) -> None:
        self.initialized = True

    def get_status(self) -> dict:
        return {"status": "active" if self.initialized else "inactive"}

    def add_knowledge(self, item: KnowledgeItemDTO) -> KnowledgeItemDTO:
        return item

    def get_knowledge(self, item_id: str):
        return None

    def search_knowledge(self, query: KnowledgeSearchQueryDTO):
        return self.return_items

    def list_knowledge(self):
        return self.return_items

def test_research_engine_initialization():
    knowledge_engine = MockKnowledgeEngine()
    engine = ResearchEngine(knowledge_engine)
    engine.initialize()
    status = engine.get_status()
    assert status["engine"] == "ResearchEngine"
    assert status["status"] == "active"

def test_research_local_hit():
    item = KnowledgeItemDTO(
        id="k1",
        title="Python Grundlagen",
        category="Fachwissen",
        content="Python ist eine Programmiersprache.",
        tags=["python", "programmieren"]
    )
    knowledge_engine = MockKnowledgeEngine(return_items=[item])
    engine = ResearchEngine(knowledge_engine)
    engine.initialize()

    query = ResearchQueryDTO(query="Python", category="Fachwissen")
    result = engine.research(query)

    assert result.found_locally is True
    assert len(result.local_results) == 1
    assert result.local_results[0].title == "Python Grundlagen"
    assert len(result.evaluations) == 1
    assert result.evaluations[0].reliability_score == 1.0
    assert "Python ist eine Programmiersprache." in result.summary

def test_research_external_fallback():
    knowledge_engine = MockKnowledgeEngine(return_items=[])
    engine = ResearchEngine(knowledge_engine)
    engine.initialize()

    query = ResearchQueryDTO(query="Quantencomputing", include_external=True)
    result = engine.research(query)

    assert result.found_locally is False
    assert len(result.local_results) == 0
    assert len(result.external_sources) > 0
    assert len(result.evaluations) > 0
    assert result.evaluations[0].reliability_score > 0
    assert "Externe Recherche" in result.summary

def test_research_no_external():
    knowledge_engine = MockKnowledgeEngine(return_items=[])
    engine = ResearchEngine(knowledge_engine)
    engine.initialize()

    query = ResearchQueryDTO(query="Unbekannt", include_external=False)
    result = engine.research(query)

    assert result.found_locally is False
    assert len(result.local_results) == 0
    assert len(result.external_sources) == 0
    assert len(result.evaluations) == 0
    assert "Keine lokalen oder externen Ergebnisse" in result.summary