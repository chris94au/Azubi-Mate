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


class LLMException(AzubiMateException):
    """Raised when an error occurs during LLM interaction."""
    pass