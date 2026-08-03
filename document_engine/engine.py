# document_engine/engine.py
import os
from typing import Any, Dict, Optional
from azubi_mate_core import (
    DocumentEngineInterface,
    DocumentExportRequestDTO,
    DocumentExportResultDTO,
    ValidationException,
    logger,
)

class DocumentEngine(DocumentEngineInterface):
    """Implementation of the Document Engine for exporting reports and documents (PDF, Word, etc.)."""

    def __init__(self, output_dir: Optional[str] = None) -> None:
        self.output_dir = output_dir or "exports"
        self._initialized = False

    def initialize(self) -> None:
        logger.info("Initializing Document Engine...")
        os.makedirs(self.output_dir, exist_ok=True)
        self._initialized = True
        logger.info("Document Engine initialized successfully.")

    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": "DocumentEngine",
            "status": "active" if self._initialized else "inactive",
            "output_dir": self.output_dir,
        }

    def export_document(self, request: DocumentExportRequestDTO) -> DocumentExportResultDTO:
        if not request.content or not request.title:
            raise ValidationException("Content and title are required for document export.")

        logger.info(f"Exporting document '{request.title}' in format '{request.format}'...")

        safe_title = "".join([c if c.isalnum() else "_" for c in request.title]).strip("_")
        filename = f"{safe_title}.{request.format.lower()}"
        file_path = os.path.join(self.output_dir, filename)

        try:
            os.makedirs(self.output_dir, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"=== {request.title} ===\n\n")
                f.write(request.content)
                if request.metadata:
                    f.write("\n\n--- Metadata ---\n")
                    for k, v in request.metadata.items():
                        f.write(f"{k}: {v}\n")

            logger.info(f"Document successfully exported to {file_path}")
            return DocumentExportResultDTO(
                file_path=file_path,
                format=request.format,
                success=True,
                message=f"Document successfully exported to {file_path}",
            )
        except Exception as e:
            logger.error(f"Failed to export document: {e}")
            return DocumentExportResultDTO(
                file_path=None,
                format=request.format,
                success=False,
                message=f"Export failed: {str(e)}",
            )