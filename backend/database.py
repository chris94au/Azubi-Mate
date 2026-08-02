# backend/database.py
import sqlite3
from pathlib import Path
from typing import Generator
from azubi_mate_core import config, logger, AzubiMateException

class DatabaseManager:
    """Manages SQLite database connections, initialization, and migrations."""

    def __init__(self, db_path: str = None) -> None:
        self.db_path = db_path or config.database_path

    def get_connection(self) -> sqlite3.Connection:
        """Opens and returns a SQLite database connection with row factory enabled."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database at {self.db_path}: {e}")
            raise AzubiMateException(f"Database connection error: {e}")

    def initialize_database(self) -> None:
        """Initializes the database schema and migration tracking table."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logger.info("Database schema initialized successfully.")
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Failed to initialize database schema: {e}")
            raise AzubiMateException(f"Database initialization error: {e}")
        finally:
            conn.close()

    def run_migrations(self) -> None:
        """Runs pending database migrations."""
        self.initialize_database()
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(version) FROM schema_migrations")
            row = cursor.fetchone()
            current_version = row[0] if row and row[0] is not None else 0

            migrations = [
                {
                    "version": 1,
                    "sql": """
                        CREATE TABLE IF NOT EXISTS persistent_items (
                            id TEXT PRIMARY KEY,
                            title TEXT NOT NULL,
                            data TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """
                }
            ]

            for migration in migrations:
                v = migration["version"]
                if v > current_version:
                    logger.info(f"Applying migration version {v}...")
                    cursor.executescript(migration["sql"])
                    cursor.execute("INSERT INTO schema_migrations (version) VALUES (?)", (v,))
                    conn.commit()
                    logger.info(f"Migration version {v} applied successfully.")

        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Migration failed: {e}")
            raise AzubiMateException(f"Migration error: {e}")
        finally:
            conn.close()

db_manager = DatabaseManager()