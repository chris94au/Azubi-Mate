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