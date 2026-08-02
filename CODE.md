This file is a merged representation of the entire codebase, combined into a single document by Repomix.

<file_summary>
This section contains a summary of this file.

<purpose>
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.
</purpose>

<file_format>
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  - File path as an attribute
  - Full contents of the file
</file_format>

<usage_guidelines>
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.
</usage_guidelines>

<notes>
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)
</notes>

</file_summary>

<directory_structure>
azubi_mate_core/
  __init__.py
  config.py
  dto.py
  exceptions.py
  interfaces.py
  models.py
backend/
  api/
    __init__.py
    router.py
  __init__.py
  database.py
  dependencies.py
  exceptions.py
  main.py
  repositories.py
doc/
  architecture/
    README.md
  module_specs/
    README.md
  prompts/
    README.md
  ai_workflow.md
  ARCHITECTURE.md
  coding_guidelines.md
  DEVELOPMENT_PLAN.md
document_engine/
  __init__.py
exam_engine/
  __init__.py
frontend/
  lib/
    main.dart
  test/
    widget_test.dart
  pubspec.yaml
knowledge_engine/
  __init__.py
learning_engine/
  __init__.py
ocr_engine/
  __init__.py
report_engine/
  __init__.py
research_engine/
  __init__.py
scripts/
  __init__.py
sync_engine/
  __init__.py
tests/
  __init__.py
  test_phase_0.py
  test_phase_1.py
  test_phase_2.py
  test_phase_3.py
voice_engine/
  __init__.py
.gitignore
pytest.ini
README.md
requirements.txt
</directory_structure>

<files>
This section contains the contents of the repository's files.

<file path="backend/api/__init__.py">

</file>

<file path="backend/api/router.py">
# backend/api/router.py
from fastapi import APIRouter
from azubi_mate_core import config, NotFoundError, ValidationException, AzubiMateException

api_router = APIRouter(prefix="/api/v1")

@api_router.get("/status")
def api_status() -> dict[str, str]:
    """API status endpoint."""
    return {
        "status": "active",
        "app": config.app_name,
        "version": config.version,
    }

@api_router.get("/test-not-found")
def trigger_not_found() -> None:
    raise NotFoundError("Resource not found")

@api_router.get("/test-validation")
def trigger_validation() -> None:
    raise ValidationException("Invalid input data")

@api_router.get("/test-core-error")
def trigger_core_error() -> None:
    raise AzubiMateException("Core general error")
</file>

<file path="backend/database.py">
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
</file>

<file path="backend/dependencies.py">
# backend/dependencies.py
import logging
from azubi_mate_core import logger as core_logger

def get_logger() -> logging.Logger:
    """Dependency to provide the application logger."""
    return core_logger
</file>

<file path="backend/exceptions.py">
# backend/exceptions.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from azubi_mate_core import (
    AzubiMateException,
    NotFoundError,
    ValidationException,
    logger,
)

def register_exception_handlers(app: FastAPI) -> None:
    """Registers global exception handlers for the FastAPI application."""

    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        logger.warning(f"Not found error: {exc.message}")
        return JSONResponse(
            status_code=404,
            content={"error": "Not Found", "message": exc.message},
        )

    @app.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException) -> JSONResponse:
        logger.warning(f"Validation error: {exc.message}")
        return JSONResponse(
            status_code=422,
            content={"error": "Validation Error", "message": exc.message},
        )

    @app.exception_handler(AzubiMateException)
    async def azubi_mate_exception_handler(request: Request, exc: AzubiMateException) -> JSONResponse:
        logger.error(f"Application error: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={"error": "Application Error", "message": exc.message},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(f"Unhandled internal error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
        )
</file>

<file path="backend/repositories.py">
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
</file>

<file path="doc/architecture/README.md">
# Architecture Documents

Dieses Verzeichnis enthält vertiefende Architekturdiagramme und Architekturentscheidungen (ADRs) für das Projekt Azubi-Mate.
</file>

<file path="doc/module_specs/README.md">
# Module Specifications

Detaillierte fachliche und technische Spezifikationen der einzelnen Engines und Module (z.B. `knowledge_engine`, `report_engine`).
</file>

<file path="doc/prompts/README.md">
# Prompts

Dieses Verzeichnis speichert alle standardisierten System-Prompts und wiederkehrenden Befehle für den AI-gestützten Entwicklungsworkflow.
</file>

<file path="doc/ai_workflow.md">
# AI Workflow

## Inkrementelle Entwicklung
Die Entwicklung erfolgt streng inkrementell nach dem `DEVELOPMENT_PLAN.md`.

## Phasen-Zyklus
1. **Analyse**: Überprüfung von Architektur, Plan und Codebasis.
2. **Implementierung**: Ausschließlich Code für die aktuelle Phase erstellen.
3. **Tests**: Passende Unit- und Integration-Tests schreiben.
4. **Validierung**: Prüfen der "Definition of Done".

## Keine stillschweigenden Änderungen
Architekturabweichungen müssen explizit begründet und vor der Implementierung bestätigt werden.
</file>

<file path="doc/ARCHITECTURE.md">
# Azubi-Mate

## Modular Development Plan

### Version 2.0

# Projektvision

**Azubi-Mate** ist eine KI-gestützte Mobile-App, die Auszubildende während ihrer gesamten Ausbildung als persönlicher Lern- und Arbeitsbegleiter unterstützt.

Der Name **Mate** steht im Sinne von *Freund, Begleiter und Unterstützer*. Die App soll Auszubildende im Alltag entlasten, Wissen verfügbar machen und organisatorische Aufgaben vereinfachen.

Azubi-Mate vereint in einer einzigen modularen Anwendung:

* Wissensdatenbank
* Recherche
* Ausbildungsnachweise
* Prüfungsvorbereitung
* Lernsystem
* KI-Assistent
* Dokumentengenerator

Sämtliche Funktionen sollen aus einer gemeinsamen Benutzeroberfläche heraus verfügbar sein.

Die Anwendung soll nach dem Herunterladen der benötigten Wissensdaten vollständig offline nutzbar sein.

Aktualisierungen der Wissensdaten erfolgen unabhängig von der eigentlichen Anwendung.

---

# Entwicklungsphilosophie

Das Projekt verfolgt folgende Grundprinzipien.

## Modularität

Jedes Modul besitzt genau eine fachliche Verantwortung.

Module kommunizieren ausschließlich über definierte Interfaces.

Direkte Abhängigkeiten zwischen Fachmodulen sind nicht erlaubt.

---

## Core First

Das wichtigste Modul ist

**azubi_mate_core**

Es enthält ausschließlich

* Datentypen
* DTOs
* Interfaces
* Basisklassen
* gemeinsame Utilities
* Fehlerklassen
* Konfiguration
* Logging

Keine Geschäftslogik.

Kein anderes Modul darf eigene Kommunikationsobjekte definieren.

Alle Module verwenden ausschließlich Typen aus dem Core-Modul.

Dadurch entsteht eine konsistente, wartbare Softwarearchitektur.

---

## Erweiterbarkeit

Neue Module können jederzeit ergänzt werden.

Beispiele:

* Lernkarten
* Prüfungsstatistik
* Cloud-Synchronisierung
* Kalender
* Notizen
* Berufsschulverwaltung
* Terminplaner
* KI-Tutor
* Voice Assistant
* OCR
* Dokumentenverwaltung
* Portfolio

Neue Funktionen sollen ohne Änderungen bestehender Module integrierbar sein.

---

# Zielplattform

## Kernprodukt

**Android**

Die mobile Anwendung ist das Hauptprodukt.

---

## Weitere Plattformen

Durch Flutter soll später dieselbe Codebasis ebenfalls bereitgestellt werden für:

* iOS
* Windows
* Linux
* macOS

Die Desktop-Version dient primär als Ergänzung für längere Schreibarbeiten, Recherche und Dokumentenverwaltung.

---

# Technologiestack

## Frontend

Flutter

Gründe

* Android
* iOS
* Windows
* Linux
* macOS

mit einer gemeinsamen Codebasis.

---

## Backend

Python

FastAPI

---

## Datenbank

Lokal

SQLite

Optional

PostgreSQL

---

## Wissensdatenbank

SQLite

plus Vektorindex

---

## KI

LLM austauschbar.

Unterstützung beispielsweise für

* Gemini
* OpenAI
* Ollama
* LM Studio

über ein gemeinsames Interface.

---

## Entwicklungsumgebung

Visual Studio Code

---

## Versionsverwaltung

Git

GitHub

---

## Dokumentation

Markdown

---

# Gesamtarchitektur

```
Flutter Mobile App

        │

        ▼

Application Layer

        │

        ▼

Backend API

        │

        ▼

Module

        │

        ▼

Core
```

---

# Modulübersicht

* azubi_mate_core
* knowledge_engine
* research_engine
* report_engine
* exam_engine
* learning_engine
* voice_engine
* document_engine
* ocr_engine
* sync_engine
* backend
* frontend

---

# Modulbeschreibungen

## Core

Verantwortlich für

* Interfaces
* DTOs
* Models
* Exceptions
* Config
* Logging
* gemeinsame Datentypen

Keine Geschäftslogik.

---

## Knowledge Engine

Verwaltet

* Ausbildungsordnungen
* Ausbildungsrahmenpläne
* Gesetze
* Lernfelder
* Fachliteratur
* Glossar

Kann Wissensdaten aktualisieren.

---

## Research Engine

Durchsucht

* lokale Wissensdatenbank
* Internet
* Quellenbewertung

Erstellt

* Zusammenfassungen
* Quellenangaben

---

## Report Engine

Erstellt Ausbildungsnachweise.

Unterstützt

* Tagesberichte
* Wochenberichte
* Monatsberichte

Eingaben

* Stichpunkte
* Sprache
* Fotos
* Dokumente

Ausgabe

IHK-konforme Berichtshefte.

---

## Exam Engine

Erstellt

* Prüfungsfragen
* Karteikarten
* Multiple Choice
* offene Fragen
* komplette Probeprüfungen

Kann Lernfortschritte speichern.

---

## Learning Engine

Erstellt individuelle Lernpläne.

Berücksichtigt

* Ausbildungsberuf
* Berufsschulfächer
* persönliche Stärken
* Schwächen
* Prüfungstermine
* Lernhistorie

---

## Voice Engine

Verarbeitet

* Spracheingabe
* Diktat
* Sprache → Text

Später zusätzlich

* Text → Sprache

---

## OCR Engine

Liest

* Arbeitsblätter
* Schulunterlagen
* Bücher
* Notizen
* Fotos

---

## Document Engine

Erzeugt

* PDF
* Word-Dokumente
* Druckversionen
* Berichtshefte
* Zusammenfassungen

---

## Sync Engine

Optional

Synchronisierung über

* Cloud
* OneDrive
* Google Drive
* Nextcloud

---

## Backend

Verwaltet

* Wissensdatenbank
* APIs
* optionale Authentifizierung
* Synchronisierung

---

## Frontend

Flutter-App.

Kommuniziert ausschließlich über Backend-APIs.

Optimiert für Smartphones.

Die Benutzeroberfläche orientiert sich an einer modernen mobilen App mit schneller Navigation, Offline-Funktionalität und einfacher Bedienung im Ausbildungsalltag.

---

# Wissensdaten

Die Wissensdaten werden strikt getrennt.

## Statische Daten

* Gesetze
* Verordnungen
* Ausbildungsrahmenpläne
* IHK-Dokumente

## Dynamische Daten

* Internetquellen
* Fachartikel
* Wikipedia
* Unternehmensinformationen
* IHK-News

---

# Recherchepipeline

Benutzer

↓

Knowledge Search

↓

Lokale Wissensdatenbank

↓

Falls nichts gefunden

↓

Internetsuche

↓

Quellenbewertung

↓

KI-Zusammenfassung

↓

Antwort

---

# Ausbildungsnachweise

Pipeline

Stichpunkte

↓

KI analysiert

↓

Erkennt Tätigkeiten

↓

Erkennt Lerninhalte

↓

Ordnet Fachbegriffe zu

↓

Erzeugt vollständigen Ausbildungsnachweis

↓

Benutzer bestätigt

↓

PDF

↓

Speichern

---

# Prüfungstrainer

Kann automatisch erzeugen

* Karteikarten
* Lückentexte
* Zuordnungsaufgaben
* Multiple Choice
* offene Fragen
* komplette Probeprüfungen

---

# Zukünftige Module

Beispiele

## Kalender

* Berufsschule
* Urlaub
* Prüfungen
* Termine

---

## Notizen

* Markdown
* Bilder
* Anhänge

---

## KI-Tutor

Persönlicher Lernassistent.

---

## Statistik

Zeigt

* Lernzeit
* Fortschritt
* Noten
* Schwächen

---

## Dokumentensammlung

Speichert

* Zeugnisse
* Verträge
* Bescheinigungen
* IHK-Dokumente

---

# Entwicklungsstrategie

Das gesamte Projekt wird ausschließlich inkrementell entwickelt.

Jeder Entwicklungsschritt besteht aus exakt einer KI-Anfrage.

Jeder Entwicklungsschritt besitzt

* genau ein Entwicklungsziel,
* höchstens zehn übertragene Dateien (Quellcode, Architektur- oder Hinweisdokumente; bei Bedarf können Inhalte gebündelt werden),
* genau eine Implementierungsanfrage,
* anschließend genau eine Kontrollanfrage zur Architektur-, Qualitäts- und Integrationsprüfung.

Neue Schritte beginnen erst, wenn der vorherige Schritt erfolgreich validiert wurde.

Änderungen an Modulgrenzen oder gemeinsamen Datentypen erfolgen ausschließlich über das Core-Modul, damit alle abhängigen Komponenten konsistent bleiben.

---

# Empfohlene Repository-Struktur

```
azubi-mate/

├── azubi_mate_core/
├── knowledge_engine/
├── research_engine/
├── report_engine/
├── exam_engine/
├── learning_engine/
├── voice_engine/
├── document_engine/
├── ocr_engine/
├── sync_engine/
├── backend/
├── frontend/
├── docs/
│   ├── architecture/
│   ├── prompts/
│   ├── development_plan.md
│   ├── coding_guidelines.md
│   ├── ai_workflow.md
│   └── module_specs/
├── scripts/
└── tests/
```
</file>

<file path="doc/coding_guidelines.md">
# Coding Guidelines

## Core First Prinzip
Alle gemeinsamen Datentypen, Interfaces und Basisklassen müssen zwingend im Modul `azubi_mate_core` definiert werden. Kein Fachmodul darf eigene DTOs zur Kommunikation verwenden.

## Modularität
Jedes Modul besitzt exakt eine Verantwortung und darf keine direkten Abhängigkeiten zu anderen Fachmodulen aufweisen. Die Kommunikation erfolgt ausschließlich über die definierten Interfaces.

## Backend
- Framework: FastAPI
- Typisierung: Strikt (Python Type Hints)
- Formatierung: PEP 8 (via Black/Ruff)

## Frontend
- Framework: Flutter
- State Management: Entsprechend der Architekturvorgaben
- UI/UX: Material 3 Design-Richtlinien
</file>

<file path="doc/DEVELOPMENT_PLAN.md">
# Azubi-Mate
# Development Plan

Version: 1.0

---

# 1. Zweck dieses Dokuments

Dieses Dokument definiert den verbindlichen Entwicklungsablauf für die Anwendung **Azubi-Mate**.

Der Entwicklungsplan dient als Arbeitsgrundlage für KI-gestützte Softwareentwicklung.

Die Kombination aus:

- ARCHITECTURE.md
- DEVELOPMENT_PLAN.md
- CODE.md

bildet die vollständige Entwicklungsgrundlage.

---

# 2. Verbindliche Entwicklungsregeln

## 2.1 Architektur ist bindend

Die Datei:

ARCHITECTURE.md

ist die oberste technische Referenz.

Keine Entwicklungsphase darf:

- Modulgrenzen verändern
- Verantwortlichkeiten verschieben
- Core-Prinzipien verletzen
- neue parallele Kommunikationsmodelle einführen
- eigene DTOs außerhalb des Core-Moduls erstellen

Falls eine Architekturänderung notwendig erscheint:

STOPP.

Die Änderung muss zuerst vorgeschlagen und begründet werden.

Keine automatische Umsetzung.

---

# 3. Entwicklungsprinzip

Das Projekt wird ausschließlich inkrementell entwickelt.

Jede Entwicklungsphase:

- besitzt genau ein Ziel
- verändert nur notwendige Komponenten
- erweitert bestehende Architektur
- enthält Tests
- wird anschließend geprüft

Keine Phase darf "nebenbei" andere Bereiche modernisieren.

---

# 4. Standardablauf jeder Entwicklungsphase

Jede Phase wird exakt nach folgendem Muster durchgeführt:

## Schritt 1: Analyse

Die KI analysiert:

- ARCHITECTURE.md
- DEVELOPMENT_PLAN.md
- CODE.md

und identifiziert:

- bestehende Implementierung
- benötigte Änderungen
- betroffene Module
- Risiken

---

## Schritt 2: Implementierung

Die KI erstellt oder verändert ausschließlich notwendige Dateien.

Dabei gilt:

- bestehende funktionierende Architektur erhalten
- keine unnötigen Refactorings
- keine Komplettumbauten
- keine Technologieänderungen

---

## Schritt 3: Tests

Jede Änderung benötigt passende Tests.

Mindestens:

- Unit Tests für neue Logik
- Integration Tests für Schnittstellen
- Fehlerfälle

---

## Schritt 4: Kontrolle

Nach Abschluss:

Prüfen:

- entspricht Implementierung ARCHITECTURE.md?
- funktionieren Interfaces?
- sind Module weiterhin entkoppelt?
- sind Tests erfolgreich?

---

# 5. Definition of Done

Eine Phase gilt nur als abgeschlossen wenn:

## Architektur

- keine Architekturregel verletzt wurde
- Core weiterhin zentrale Schnittstelle bleibt

## Code

- Code funktioniert
- Code dokumentiert ist
- keine unnötigen Duplikate entstanden sind

## Tests

- neue Tests existieren
- Tests erfolgreich laufen

## Integration

- abhängige Module funktionieren weiterhin

---

# 6. Moduländerungsregeln

## Core Änderungen

Das Core-Modul ist besonders geschützt.

Änderungen an:

- Interfaces
- DTOs
- Exceptions
- Basisklassen

benötigen besondere Prüfung.

Ablauf:

1. Core ändern
2. abhängige Module aktualisieren
3. Tests ausführen
4. erst danach nächste Phase

---

# 7. Versions- und Änderungsprinzip

Breaking Changes vermeiden.

Bevorzugt:

- Erweiterungen
- neue Interfaces
- optionale Felder
- zusätzliche Services

Nicht:

- bestehende Verträge entfernen

---

# 8. Entwicklungsphasen

---

# Phase 0
# Projektgrundlage

Status:
⬜ geplant

## Ziel

Grundstruktur der Azubi-Mate Anwendung erstellen.

## Betroffene Module

- azubi_mate_core
- backend
- frontend

## Implementierung

Erstellen:

- Repository Struktur
- Python Backend Grundgerüst
- Flutter Grundgerüst
- Core Modul

## Erwartete Komponenten

Core:

- Models
- DTOs
- Interfaces
- Exceptions
- Configuration

Backend:

- FastAPI Startpunkt

Frontend:

- Flutter App Startpunkt

## Tests

- Backend startet
- Flutter App startet
- Core kann importiert werden

## Definition of Done

- Repository entspricht ARCHITECTURE.md
- Backend läuft
- Frontend läuft
- Core ist unabhängig

---

# Phase 1
# Core Architektur

Status:
⬜ geplant

## Ziel

Das zentrale Fundament aller Module implementieren.

## Betroffene Module

- azubi_mate_core

## Implementierung

Erstellen:

- gemeinsame Datentypen
- Interfaces
- Basisklassen
- Fehlerklassen
- Logging-Struktur
- Konfiguration

## Erwartete Komponenten

Beispiele:


core/
├── interfaces/
├── models/
├── dto/
├── exceptions/
├── config/
└── utils/


## Tests

- Imports
- Interface Implementierungen
- Exception Handling

## Definition of Done

- kein Fachmodul besitzt eigene Core-Strukturen
- Core enthält keine Geschäftslogik

---

# Phase 2
# Backend Basis

Status:
⬜ geplant

## Ziel

Backend-Infrastruktur bereitstellen.

## Betroffene Module

- backend
- azubi_mate_core

## Implementierung

Erstellen:

- FastAPI Anwendung
- Dependency Injection
- API Routing
- Fehlerbehandlung
- Logging

## Tests

- API Start
- Health Endpoint
- Fehlerantworten

## Definition of Done

Backend kann Module verwalten.

---

# Phase 3
# Lokale Datenhaltung

Status:
⬜ geplant

## Ziel

Persistente lokale Speicherung bereitstellen.

## Betroffene Module

- backend
- azubi_mate_core

## Implementierung

Erstellen:

- SQLite Integration
- Migration System
- Repository Pattern

Regel:

Kein Modul greift direkt auf SQLite zu.

## Tests

- Datenbank Initialisierung
- Migration
- Speichern
- Laden
- Fehlerfälle

## Definition of Done

Persistenz funktioniert unabhängig von Fachmodulen.

---

# Phase 4
# Knowledge Engine

Status:
⬜ geplant

## Ziel

Grundlage der Wissensdatenbank.

## Betroffene Module

- knowledge_engine
- azubi_mate_core

## Implementierung

Erstellen:

- Wissensobjekte
- Speicherung
- Suche Interface

Unterstützen:

- Ausbildungsordnungen
- Lerninhalte
- Fachwissen

## Tests

- Daten speichern
- Daten suchen
- Schnittstellen testen

## Definition of Done

Knowledge Engine funktioniert unabhängig.

---

# Phase 5
# Research Engine

Status:
⬜ geplant

## Ziel

Recherchepipeline implementieren.

## Betroffene Module

- research_engine
- knowledge_engine
- core

## Pipeline


Anfrage
↓
Lokale Suche
↓
Falls nicht vorhanden:
Externe Quelle
↓
Bewertung
↓
Zusammenfassung


## Tests

- lokale Treffer
- keine Treffer
- Quellenbewertung

## Definition of Done

Recherche funktioniert über Interfaces.

---

# Phase 6
# KI Integration

Status:
⬜ geplant

## Ziel

LLM unabhängig integrieren.

## Betroffene Module

- core
- backend

## Implementierung

Interface:


LLMProvider


Implementierungen:

- Ollama
- OpenAI
- Gemini

## Tests

- Provider Austausch
- Mock Provider
- Fehlerbehandlung

## Definition of Done

KI-Anbieter austauschbar.

---

# Phase 7
# Report Engine

Status:
⬜ geplant

## Ziel

Ausbildungsnachweise erzeugen.

## Betroffene Module

- report_engine
- document_engine

## Funktionen

- Tagesberichte
- Wochenberichte
- Monatsberichte

Pipeline:


Stichpunkte
↓
Analyse
↓
Fachbegriffe
↓
Bericht
↓
Dokument


## Tests

- Bericht erzeugen
- Export testen

---

# Phase 8
# Exam Engine

Status:
⬜ geplant

## Ziel

Prüfungstrainer erstellen.

## Betroffene Module

- exam_engine
- learning_engine

## Funktionen

- Karteikarten
- Multiple Choice
- offene Fragen
- Prüfungssimulation

## Tests

- Fragengenerierung
- Bewertung
- Fortschritt

---

# Phase 9
# Learning Engine

Status:
⬜ geplant

## Ziel

Individuelle Lernplanung.

## Betroffene Module

- learning_engine

## Funktionen

- Lernplan
- Schwächenanalyse
- Fortschritt

## Tests

- Planerstellung
- Anpassung

---

# Phase 10
# Frontend Anwendung

Status:
⬜ geplant

## Ziel

Mobile/Desktop App.

## Betroffene Module

- frontend

## Funktionen

- Dashboard
- Wissen
- Berichtsheft
- Lernen
- KI-Assistent

## Tests

- Navigation
- API Kommunikation

---

# Phase 11
# Dokumente und Export

Status:
⬜ geplant

## Ziel

Dokumentenverwaltung.

## Betroffene Module

- document_engine

## Funktionen

- PDF
- Word
- Druck
- Speicherung

---

# Phase 12
# Erweiterungsmodule

Status:
⬜ geplant

## Ziel

Optionale Module.

Beispiele:

- OCR
- Voice
- Sync
- Kalender
- Notizen

Jedes Modul folgt weiterhin:

Core First Prinzip.

---

# 9. Abschlusskriterien Gesamtprojekt

Azubi-Mate gilt als erfolgreich implementiert wenn:

## Funktion

- Wissen verwalten
- Lernen unterstützen
- Berichte erzeugen
- KI-Assistent vorhanden

## Architektur

- Module getrennt
- Core zentral
- KI austauschbar

## Plattform

- Android
- iOS
- Windows

## Qualität

- Tests vorhanden
- Dokumentation vorhanden
- Erweiterbarkeit gewährleistet

---

Ende DEVELOPMENT_PLAN.md
</file>

<file path="document_engine/__init__.py">
"""
Azubi-Mate Document Engine
"""
</file>

<file path="exam_engine/__init__.py">
"""
Azubi-Mate Exam Engine
"""
</file>

<file path="frontend/lib/main.dart">
import 'package:flutter/material.dart';

void main() {
  runApp(const AzubiMateApp());
}

class AzubiMateApp extends StatelessWidget {
  const AzubiMateApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Azubi-Mate',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0D47A1)),
        useMaterial3: true,
      ),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Azubi-Mate Dashboard'),
      ),
      body: const Center(
        child: Text('Willkommen bei Azubi-Mate!'),
      ),
    );
  }
}
</file>

<file path="frontend/test/widget_test.dart">
import 'package:flutter_test/flutter_test.dart';
import 'package:azubi_mate/main.dart';

void main() {
  testWidgets('App starts and shows welcome message', (WidgetTester tester) async {
    await tester.pumpWidget(const AzubiMateApp());

    expect(find.text('Azubi-Mate Dashboard'), findsOneWidget);
    expect(find.text('Willkommen bei Azubi-Mate!'), findsOneWidget);
  });
}
</file>

<file path="frontend/pubspec.yaml">
name: azubi_mate
description: "Azubi-Mate: KI-gestützte Mobile-App für Auszubildende."
publish_to: 'none'
version: 0.1.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
</file>

<file path="knowledge_engine/__init__.py">
"""
Azubi-Mate Knowledge Engine
"""
</file>

<file path="learning_engine/__init__.py">
"""
Azubi-Mate Learning Engine
"""
</file>

<file path="ocr_engine/__init__.py">
"""
Azubi-Mate OCR Engine
"""
</file>

<file path="report_engine/__init__.py">
"""
Azubi-Mate Report Engine
"""
</file>

<file path="research_engine/__init__.py">
"""
Azubi-Mate Research Engine
"""
</file>

<file path="scripts/__init__.py">

</file>

<file path="sync_engine/__init__.py">
"""
Azubi-Mate Sync Engine
"""
</file>

<file path="tests/__init__.py">
"""
Azubi-Mate Test Suite
"""
</file>

<file path="tests/test_phase_1.py">
# tests/test_phase_1.py
import pytest
from azubi_mate_core import (
    CoreModel,
    BaseDTO,
    BaseEngine,
    AzubiMateException,
    ConfigurationError,
    config,
    logger,
)

class DummyEngine(BaseEngine):
    def initialize(self) -> None:
        pass

    def get_status(self) -> dict:
        return {"status": "active"}

def test_core_models_and_dtos() -> None:
    model = CoreModel()
    assert model is not None
    dto = BaseDTO()
    assert dto is not None

def test_interface_implementation() -> None:
    engine = DummyEngine()
    engine.initialize()
    status = engine.get_status()
    assert status["status"] == "active"

def test_exceptions() -> None:
    exc = AzubiMateException("Base error")
    assert exc.message == "Base error"
    
    cfg_exc = ConfigurationError("Config error")
    assert cfg_exc.message == "Config error"
    assert isinstance(cfg_exc, AzubiMateException)

def test_config_and_logging() -> None:
    assert config.app_name is not None
    assert logger is not None
</file>

<file path="tests/test_phase_2.py">
# tests/test_phase_2.py
from fastapi.testclient import TestClient
from backend.main import app
from azubi_mate_core.config import config

client = TestClient(app)

def test_health_and_api_status() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    response_api = client.get("/api/v1/status")
    assert response_api.status_code == 200
    assert response_api.json()["status"] == "active"

def test_error_responses() -> None:
    response_nf = client.get("/api/v1/test-not-found")
    assert response_nf.status_code == 404
    assert response_nf.json()["error"] == "Not Found"

    response_val = client.get("/api/v1/test-validation")
    assert response_val.status_code == 422
    assert response_val.json()["error"] == "Validation Error"

    response_err = client.get("/api/v1/test-core-error")
    assert response_err.status_code == 400
    assert response_err.json()["error"] == "Application Error"
</file>

<file path="tests/test_phase_3.py">
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
</file>

<file path="voice_engine/__init__.py">

</file>

<file path=".gitignore">
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.env
*.sqlite3

# Flutter
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
build/
.packages
.pub-cache/
.pub/

# IDE / OS
.vscode/
.idea/
*.swp
.DS_Store
</file>

<file path="pytest.ini">
[pytest]
pythonpath = .
testpaths = tests
addopts = -v
</file>

<file path="requirements.txt">
fastapi>=0.104.1
uvicorn>=0.24.0
pydantic>=2.5.2
pydantic-settings>=2.1.0
pytest>=7.4.3
httpx>=0.25.1
</file>

<file path="azubi_mate_core/dto.py">
# azubi_mate_core/dto.py
from pydantic import BaseModel, ConfigDict

class BaseDTO(BaseModel):
    """Base Data Transfer Object for all module communications."""
    model_config = ConfigDict(from_attributes=True)
</file>

<file path="azubi_mate_core/exceptions.py">
# azubi_mate_core/exceptions.py
class AzubiMateException(Exception):
    """Base exception for all Azubi-Mate errors."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ConfigurationError(AzubiMateException):
    """Raised when there is an error in application configuration."""
    pass


class NotFoundError(AzubiMateException):
    """Raised when a requested resource is not found."""
    pass


class ValidationException(AzubiMateException):
    """Raised when validation fails for input data or domain logic."""
    pass
</file>

<file path="azubi_mate_core/models.py">
# azubi_mate_core/models.py
from pydantic import BaseModel, ConfigDict

class CoreModel(BaseModel):
    """Base model for all internal domain models."""
    model_config = ConfigDict(from_attributes=True)
</file>

<file path="backend/__init__.py">
# backend/api/__init__.py
</file>

<file path="backend/main.py">
# backend/main.py
from fastapi import FastAPI
from azubi_mate_core.config import config, logger
from backend.exceptions import register_exception_handlers
from backend.api.router import api_router

app = FastAPI(
    title=config.app_name,
    version=config.version,
    debug=config.debug,
)

# Register global error handlers
register_exception_handlers(app)

# Include API routers
app.include_router(api_router)

@app.on_event("startup")
def startup_event() -> None:
    logger.info(f"Starting {config.app_name} v{config.version}...")

@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint to verify backend status."""
    return {
        "status": "ok", 
        "app": config.app_name, 
        "version": config.version,
    }
</file>

<file path="tests/test_phase_0.py">
from fastapi.testclient import TestClient
from backend.main import app
from azubi_mate_core.config import config
from azubi_mate_core.exceptions import AzubiMateException

client = TestClient(app)

def test_backend_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok", 
        "app": config.app_name, 
        "version": config.version
    }

def test_core_imports_and_usage() -> None:
    exc = AzubiMateException("Test Error")
    assert exc.message == "Test Error"
    assert config.version == "0.1.0"
</file>

<file path="README.md">
# Azubi-Mate

**Azubi-Mate** ist eine KI-gestützte Mobile-App, die Auszubildende während ihrer gesamten Ausbildung als persönlicher Lern- und Arbeitsbegleiter unterstützt.

## Projektstruktur
Die Architektur basiert auf einem modularen Core-First-Ansatz. Das wichtigste Modul ist `azubi_mate_core`, welches ausschließlich Datentypen, Interfaces und gemeinsame Utilities bereitstellt.

## Lokale Entwicklung

### Backend (Python/FastAPI)
```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Backend starten
uvicorn backend.main:app --reload

# Tests ausführen
pytest tests/
```

### Frontend (Flutter)

```Bash

cd frontend

# Abhängigkeiten laden
flutter pub get

# App starten
flutter run

# Tests ausführen
flutter test
```
</file>

<file path="azubi_mate_core/__init__.py">
# azubi_mate_core/__init__.py
"""
Azubi-Mate Core Module
Contains shared data types, interfaces, base classes, exceptions, and configuration.
"""
from .models import CoreModel
from .dto import BaseDTO
from .interfaces import BaseEngine, BaseRepository
from .exceptions import (
    AzubiMateException,
    ConfigurationError,
    NotFoundError,
    ValidationException,
)
from .config import config, AppConfig, logger, setup_logging

__all__ = [
    "CoreModel",
    "BaseDTO",
    "BaseEngine",
    "BaseRepository",
    "AzubiMateException",
    "ConfigurationError",
    "NotFoundError",
    "ValidationException",
    "config",
    "AppConfig",
    "logger",
    "setup_logging",
]
</file>

<file path="azubi_mate_core/config.py">
# azubi_mate_core/config.py
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    """Core application configuration."""
    app_name: str = "Azubi-Mate API"
    debug: bool = False
    version: str = "0.1.0"
    log_level: str = "INFO"
    database_path: str = "azubi_mate.db"
    
    model_config = SettingsConfigDict(env_prefix="AZUBI_")

config = AppConfig()

def setup_logging() -> logging.Logger:
    """Configures and returns the root logger for Azubi-Mate."""
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    return logging.getLogger("azubi_mate")

logger = setup_logging()
</file>

<file path="azubi_mate_core/interfaces.py">
# azubi_mate_core/interfaces.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

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
</file>

</files>
