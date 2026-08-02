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