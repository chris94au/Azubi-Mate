# knowledge_engine/repository.py
import json
from typing import List, Optional
from azubi_mate_core import BaseRepository, ValidationException
from azubi_mate_core.dto import KnowledgeItemDTO, KnowledgeSearchQueryDTO
from backend.database import db_manager

class KnowledgeRepository(BaseRepository[KnowledgeItemDTO]):
    """SQLite repository for Knowledge items."""

    def __init__(self) -> None:
        self._init_table()

    def _init_table(self) -> None:
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise ValidationException(f"Failed to initialize knowledge table: {e}")
        finally:
            conn.close()

    def add(self, entity: KnowledgeItemDTO) -> KnowledgeItemDTO:
        if not entity.id or not entity.title or not entity.category:
            raise ValidationException("Knowledge item must have id, title, and category.")
        
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO knowledge_items (id, title, category, content, tags)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    category = excluded.category,
                    content = excluded.content,
                    tags = excluded.tags
                """,
                (entity.id, entity.title, entity.category, entity.content, json.dumps(entity.tags))
            )
            conn.commit()
            return entity
        except Exception as e:
            conn.rollback()
            raise ValidationException(f"Failed to save knowledge item: {e}")
        finally:
            conn.close()

    def get_by_id(self, entity_id: str) -> Optional[KnowledgeItemDTO]:
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, category, content, tags FROM knowledge_items WHERE id = ?", (entity_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return KnowledgeItemDTO(
                id=row["id"],
                title=row["title"],
                category=row["category"],
                content=row["content"],
                tags=json.loads(row["tags"])
            )
        finally:
            conn.close()

    def list_all(self) -> List[KnowledgeItemDTO]:
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, category, content, tags FROM knowledge_items")
            rows = cursor.fetchall()
            items = []
            for row in rows:
                items.append(
                    KnowledgeItemDTO(
                        id=row["id"],
                        title=row["title"],
                        category=row["category"],
                        content=row["content"],
                        tags=json.loads(row["tags"])
                    )
                )
            return items
        finally:
            conn.close()

    def delete(self, entity_id: str) -> bool:
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM knowledge_items WHERE id = ?", (entity_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise ValidationException(f"Failed to delete knowledge item: {e}")
        finally:
            conn.close()

    def search(self, query_dto: KnowledgeSearchQueryDTO) -> List[KnowledgeItemDTO]:
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            search_term = f"%{query_dto.query}%"
            if query_dto.category:
                cursor.execute(
                    """
                    SELECT id, title, category, content, tags 
                    FROM knowledge_items 
                    WHERE category = ? AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)
                    LIMIT ?
                    """,
                    (query_dto.category, search_term, search_term, search_term, query_dto.limit)
                )
            else:
                cursor.execute(
                    """
                    SELECT id, title, category, content, tags 
                    FROM knowledge_items 
                    WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                    LIMIT ?
                    """,
                    (search_term, search_term, search_term, query_dto.limit)
                )
            rows = cursor.fetchall()
            items = []
            for row in rows:
                items.append(
                    KnowledgeItemDTO(
                        id=row["id"],
                        title=row["title"],
                        category=row["category"],
                        content=row["content"],
                        tags=json.loads(row["tags"])
                    )
                )
            return items
        finally:
            conn.close()