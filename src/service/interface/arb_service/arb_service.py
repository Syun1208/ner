from abc import ABC, abstractmethod

class ARBService(ABC):
    @abstractmethod
    def get_responding(self, user_id: str, session_id: str, message: str) -> str:
        pass