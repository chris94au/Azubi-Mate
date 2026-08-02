# tests/test_phase_3.py
import os
import pytest
from backend.database import DatabaseManager
from backend.repositories import SQLiteItemRepository, ItemModel
from azubi_mate_core import ValidationException, AzubiMateException

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_azubi.db"
    manager = DatabaseManager(db_path=str(db_file))
    manager.initialize_database()
    manager.run_migrations()
    return manager

def test_database_initialization_and_migration(temp_db):
    conn = temp_db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_migrations'")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='persistent_items'")
    assert cursor.fetchone() is not None
    conn.close()

def test_repository_save_and_load(tmp_path):
    db_file = tmp_path / "test_repo.db"
    from backend import database
    original_path = database.db_manager.db_path
    database.db_manager.db_path = str(db_file)
    
    try:
        repo = SQLiteItemRepository()
        item = ItemModel(id="1", title="Test Item", content="Test Content")
        
        saved = repo.add(item)
        assert saved.id == "1"
        
        loaded = repo.get_by_id("1")
        assert loaded is not None
        assert loaded.title == "Test Item"
        assert loaded.content == "Test Content"
        
        items = repo.list_all()
        assert len(items) == 1
        assert items[0].id == "1"
        
        success = repo.delete("1")
        assert success is True
        assert repo.get_by_id("1") is None
        assert len(repo.list_all()) == 0
        
    finally:
        database.db_manager.db_path = original_path

def test_repository_error_handling(tmp_path):
    db_file = tmp_path / "test_error.db"
    from backend import database
    original_path = database.db_manager.db_path
    database.db_manager.db_path = str(db_file)
    
    try:
        repo = SQLiteItemRepository()
        
        with pytest.raises(ValidationException):
            repo.add(ItemModel(id="", title="", content=""))
            
    finally:
        database.db_manager.db_path = original_path