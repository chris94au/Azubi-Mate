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