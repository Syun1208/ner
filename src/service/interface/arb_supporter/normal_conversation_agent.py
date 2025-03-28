from abc import ABC, abstractmethod

class NormalConversationAgent(ABC):

    @abstractmethod
    def start_conversation(self, user_id: int, session_id: str) -> None:
        pass


    @abstractmethod
    def responding(self, user_id: int, session_id: str, message: str) -> str:
        pass
    