# knowledge_engine/engine.py
from typing import Any, Dict, List, Optional
from azubi_mate_core import KnowledgeEngineInterface, KnowledgeItemDTO, KnowledgeSearchQueryDTO, logger
from knowledge_engine.repository import KnowledgeRepository

class KnowledgeEngine(KnowledgeEngineInterface):
    """Implementation of the Knowledge Engine."""

    def __init__(self, repository: Optional[KnowledgeRepository] = None) -> None:
        self.repository = repository or KnowledgeRepository()
        self._initialized = False

    def initialize(self) -> None:
        logger.info("Initializing Knowledge Engine...")
        self._initialized = True
        logger.info("Knowledge Engine initialized successfully.")

    def get_status(self) -> Dict[str, Any]:
        items_count = len(self.repository.list_all())
        return {
            "engine": "KnowledgeEngine",
            "status": "active" if self._initialized else "inactive",
            "items_count": items_count,
        }

    def add_knowledge(self, item: KnowledgeItemDTO) -> KnowledgeItemDTO:
        logger.info(f"Adding knowledge item: {item.id} - {item.title}")
        return self.repository.add(item)

    def get_knowledge(self, item_id: str) -> Optional[KnowledgeItemDTO]:
        return self.repository.get_by_id(item_id)

    def search_knowledge(self, query: KnowledgeSearchQueryDTO) -> List[KnowledgeItemDTO]:
        logger.info(f"Searching knowledge with query: '{query.query}', category: {query.category}")
        return self.repository.search(query)

    def list_knowledge(self) -> List[KnowledgeItemDTO]:
        return self.repository.list_all()