from abc import ABC, abstractmethod
from typing import Dict


class ConfirmationAgent(ABC):
    

    @abstractmethod
    def get_decision(self, query: str) -> Dict[str, str]:
        """
        Abstract method to process the user's query and return a decision.

        Args:
            query (str): The user's query.

        Returns:
            Dict[str, str]: A dictionary containing the decision or confirmation result.
        """
        pass