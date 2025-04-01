from abc import ABC, abstractmethod
from src.model.Alpha_metadata import AlphaMetadata
class FunctionCallingConversationAgent(ABC):

    @abstractmethod
    def start_conversation(self, user_id: str) -> None:
        pass

    @abstractmethod
    def get_response(self, user_id: int, message: str) -> AlphaMetadata:
        pass
    