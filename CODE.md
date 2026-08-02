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
  __init__.py
  main.py
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
voice_engine/
  __init__.py
.gitignore
pytest.ini
README.md
requirements.txt
</directory_structure>

<files>
This section contains the contents of the repository's files.

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

<file path="azubi_mate_core/__init__.py">
# azubi_mate_core/__init__.py
"""
Azubi-Mate Core Module
Contains shared data types, interfaces, base classes, exceptions, and configuration.
"""
from .models import CoreModel
from .dto import BaseDTO
from .interfaces import BaseEngine
from .exceptions import AzubiMateException, ConfigurationError
from .config import config, AppConfig, logger, setup_logging

__all__ = [
    "CoreModel",
    "BaseDTO",
    "BaseEngine",
    "AzubiMateException",
    "ConfigurationError",
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
</file>

<file path="azubi_mate_core/interfaces.py">
# azubi_mate_core/interfaces.py
from abc import ABC, abstractmethod
from typing import Any, Dict

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
</file>

<file path="azubi_mate_core/models.py">
# azubi_mate_core/models.py
from pydantic import BaseModel, ConfigDict

class CoreModel(BaseModel):
    """Base model for all internal domain models."""
    model_config = ConfigDict(from_attributes=True)
</file>

<file path="backend/__init__.py">

</file>

<file path="backend/main.py">
from fastapi import FastAPI
from azubi_mate_core.config import config

app = FastAPI(
    title=config.app_name,
    version=config.version,
    debug=config.debug
)

@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint to verify backend status."""
    return {
        "status": "ok", 
        "app": config.app_name, 
        "version": config.version
    }
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

</files>
