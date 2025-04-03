from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class NerAgent(ABC):
    """
    Abstract base class for Named Entity Recognition (NER) operations.
    This class defines the interface for NER processing in the system.
    """
    
    @abstractmethod
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract specific types of entities from the input text.
        
        Args:
            text (str): The input text to process
            entity_types (Optional[List[str]]): List of entity types to extract. 
                                              If None, extract all supported types.
        
        Returns:
            List[Dict[str, Any]]: List of extracted entities with their properties
        """
        pass

    @abstractmethod
    def get_entity_types(self) -> List[str]:
        """
        Get the list of entity types that this NER agent can recognize.
        
        Returns:
            List[str]: List of supported entity types
        """
        pass