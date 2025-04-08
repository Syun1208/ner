from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ARBDBService(ABC):
    """
    Abstract base class defining interface for NoSQL database operations.
    """

    @abstractmethod
    def get(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document from the specified collection matching the query.

        Args:
            user_id: User ID to query

        Returns:
            Optional[Dict[str, Any]]: Matching document if found, None otherwise
        """
        pass

    @abstractmethod
    def insert(self, user_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Insert a new document into the specified collection.

        Args:
            user_id: User ID to insert into
            metadata: Metadata to insert

        Returns:
            bool: True if insert was successful, False otherwise
        """
        pass

    @abstractmethod
    def update(self, user_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update documents in the collection matching the query.

        Args:
            user_id: User ID to update
            metadata: Metadata to update

        Returns:
            bool: True if update was successful, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """
        Delete documents from the collection matching the query.

        Args:
            user_id: User ID to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass

