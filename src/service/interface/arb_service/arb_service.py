from abc import ABC, abstractmethod
from src.model.Alpha_metadata import AlphaMetadata
class ARBService(ABC):
    @abstractmethod
    def get_responding(self, user_id: str, session_id: str, message: str) -> str:
        pass
    
    @abstractmethod
    def get_alpha_response(self, user_id: str, message: str) -> AlphaMetadata:
        pass