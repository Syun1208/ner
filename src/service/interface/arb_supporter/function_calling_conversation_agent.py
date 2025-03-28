from abc import ABC, abstractmethod
from src.model.Alpha_metadata import AlphaMetadata
class FunctionCallingConversationAgent(ABC):

    @abstractmethod
    def start_conversation(self, user_id: str) -> None:
        pass

    @abstractmethod
    def responding(self, user_id: int, session_id: str, message: str) -> str:
        pass

    @abstractmethod
    def alpha_responding(self, user_id: int, message: str) -> AlphaMetadata:
        pass
    