from abc import ABC, abstractmethod
from typing import List

class TaskDetectionAgent(ABC):
    """
    Abstract base class for task detection.
    """


    def detect_task(self, query: str) -> List[str]:
        """
        Detect the task from the given query.

        Args:
            query (str): The input query from the user.

        Returns:
            Dict[str, str]: A dictionary containing detected task details.
        """
        pass