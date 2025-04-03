from abc import ABC, abstractmethod

class NormalConversationAgent(ABC):

    @abstractmethod
    def chat(self, message: str) -> str:
        pass
    