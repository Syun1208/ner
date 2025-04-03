from abc import ABC, abstractmethod
from typing import Dict, Any

class FunctionCallingAgent(ABC):
    """
    Abstract base class for Function Calling operations.
    This class defines the interface for handling function calls in the system.
    """
    
    @abstractmethod
    def call_function(self, message: str) -> Dict[str, Any]:
        """
        Call a registered function with the given message.
        
        Args:
            message (str): The message to pass to the function
            
        Returns:
            Dict[str, Any]: Result of the function execution
        """
        pass
    
