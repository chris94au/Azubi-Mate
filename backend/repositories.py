# backend/repositories.py
import json
from typing import List, Optional
from azubi_mate_core import BaseRepository, CoreModel, ValidationException, NotFoundError
from backend.database import db_manager

class ItemModel(CoreModel):
    """Domain model for persistent items."""
    id: str
    title: str
    content: str

class SQLiteItemRepository(BaseRepository[ItemModel]):
    """SQLite implementation of the repository pattern for ItemModel."""

    def __init__(self) -> None:
        db_manager.run_migrations()

    def add(self, entity: ItemModel) -> ItemModel:
        """Saves or updates an item in the SQLite database."""
        if not entity.id or not entity.title:
            raise ValidationException("Item must have a valid id and title.")
        
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO persistent_items (id, title, data)
                VALUES (?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    data = excluded.data
                """,
                (entity.id, entity.title, json.dumps({"content": entity.content}))
            )
            conn.commit()
            return entity
        except Exception as e:
            conn.rollback()
            raise ValidationException(f"Failed to save item: {e}")
        finally:
            conn.close()

    def get_by_id(self, entity_id: str) -> Optional[ItemModel]:
        """Retrieves an item by its id."""
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, data FROM persistent_items WHERE id = ?", (entity_id,))
            row = cursor.fetchone()
            if not row:
                return None
            data_dict = json.loads(row["data"])
            return ItemModel(
                id=row["id"],
                title=row["title"],
                content=data_dict.get("content", "")
            )
        finally:
            conn.close()

    def list_all(self) -> List[ItemModel]:
        """Retrieves all items from the database."""
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, data FROM persistent_items")
            rows = cursor.fetchall()
            items = []
            for row in rows:
                data_dict = json.loads(row["data"])
                items.append(
                    ItemModel(
                        id=row["id"],
                        title=row["title"],
                        content=data_dict.get("content", "")
                    )
                )
            return items
        finally:
            conn.close()

    def delete(self, entity_id: str) -> bool:
        """Deletes an item by its id."""
        conn = db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM persistent_items WHERE id = ?", (entity_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise ValidationException(f"Failed to delete item: {e}")
        finally:
            conn.close()