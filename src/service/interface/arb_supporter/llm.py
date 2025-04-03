from abc import ABC, abstractmethod
from typing import Dict, Any, List


class LLM(ABC):
    
    @abstractmethod
    def invoke(
        self,
        message: List[Dict[str, str]],
        tools: Dict[str, Any] = None,
        format_schema: Dict[str, Any] = None,
        endpoint: str = '/api/chat'
    ) -> Dict[str, str]:
        
        pass