import json
from typing import Dict, Any, Optional


from src.service.interface.arb_supporter.nosql_dabase import NoSQLDatabase



class JsonDatabase(NoSQLDatabase):
    """
    Implementation of NoSQLDatabase interface using JSON file storage.
    """

    def __init__(
        self, 
        json_file_path: str
    ) -> None:
        """
        Initialize JsonDatabase with path to JSON file.

        Args:
            json_file_path (str): Path to the JSON file to use as storage
        """
        self.json_file_path = json_file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create JSON file if it doesn't exist."""
        try:
            with open(self.json_file_path, 'r') as f:
                json.load(f)
        except FileNotFoundError:
            with open(self.json_file_path, 'w') as f:
                json.dump({}, f)

    def get(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user data from JSON file.

        Args:
            user_id: User ID to query

        Returns:
            Optional[Dict[str, Any]]: User data if found, None otherwise
        """
        with open(self.json_file_path, 'r') as f:
            data = json.load(f)
            return data.get(user_id)

    def insert(self, user_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Insert new user data into JSON file.

        Args:
            user_id: User ID to insert
            metadata: Metadata to insert

        Returns:
            bool: True if insert successful, False otherwise
        """
        try:
            with open(self.json_file_path, 'r') as f:
                data = json.load(f)
            
            data[user_id] = metadata

            with open(self.json_file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False

    def update(self, user_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update existing user data in JSON file.

        Args:
            user_id: User ID to update
            metadata: Updated metadata

        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            with open(self.json_file_path, 'r') as f:
                data = json.load(f)
            
            if user_id in data:
                data[user_id].update(metadata)
                with open(self.json_file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                return True
            return False
        except Exception:
            return False

    def delete(self, user_id: str) -> bool:
        """
        Delete user data from JSON file.

        Args:
            user_id: User ID to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            with open(self.json_file_path, 'r') as f:
                data = json.load(f)
            
            if user_id in data:
                del data[user_id]
                with open(self.json_file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                return True
            return False
        except Exception:
            return False
