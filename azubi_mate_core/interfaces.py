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