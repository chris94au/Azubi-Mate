from abc import ABC, abstractmethod

class BaseEngine(ABC):
    """Base interface for all engines in Azubi-Mate."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initializes the engine."""
        pass