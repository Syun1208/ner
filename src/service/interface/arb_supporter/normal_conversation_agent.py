from abc import ABC, abstractmethod

class NormalConversationAgent(ABC):

    @abstractmethod
    def start_conversation(self, user_id: str) -> None:
        pass

    @abstractmethod
    def send_message(self, user_id: str, message: str) -> None:
        pass

    @abstractmethod
    def receive_message(self, user_id: str) -> str:
        pass

    @abstractmethod
    def end_conversation(self, user_id: str) -> None:
        pass
    