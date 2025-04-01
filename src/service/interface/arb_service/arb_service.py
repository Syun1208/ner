from abc import ABC, abstractmethod
from src.model.Alpha_metadata import AlphaMetadata
class ARBService(ABC):    
    @abstractmethod
    def chat(self, user_id: str, message: str) -> AlphaMetadata:
        pass