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
