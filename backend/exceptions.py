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