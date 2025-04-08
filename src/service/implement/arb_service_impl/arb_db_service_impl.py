import json
import os
from typing import Dict, Any, Optional, List


from src.service.interface.arb_service.arb_db_service import ARBDBService
from src.utils.utils import load_json, to_json


class ARBDBServiceImpl(ARBDBService):
    """
    Implementation of NoSQLDatabase interface using JSON file storage.
    """

    def __init__(
        self, 
        database_path: str
    ) -> None:
        """
        Initialize JsonDatabase with path to JSON file.

        Args:
            json_file_path (str): Path to the JSON file to use as storage
        """
        self.database_path = database_path
        self.__ensure_folder_exists()
        self.__init_database()

    def __init_database(self) -> None:
        to_json(data={}, path=self.database_path)

    def __ensure_folder_exists(self) -> None:
        if not os.path.exists(os.path.dirname(self.database_path)):
            os.makedirs(os.path.dirname(self.database_path))
    
    def get(self, user_id: str) -> Dict[str, List[str]]:
        """
        Retrieve user data from JSON file.

        Args:
            user_id: User ID to query

        Returns:
            Dict[str, List[str]]: User data if found, None otherwise
        """
        
        data = load_json(path=self.database_path)
        if not data:
            return data
        return data.get(user_id)

    def insert(self, user_id: str, metadata: List[Dict[str, Any]]) -> bool:
        """
        Insert new user data into JSON file.

        Args:
            user_id: User ID to insert
            metadata: Metadata to insert

        Returns:
            bool: True if insert successful, False otherwise
        """
        try:
            data = load_json(self.database_path)
            data[user_id] = metadata

            to_json(data=data, path=self.database_path)   
            
            return True
       
        except Exception as e:
            print('🤖 insert error: ', e)
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
            data = load_json(path=self.database_path)
            
            if user_id in list(data.keys()):
                data[user_id] = metadata
                to_json(data=data, path=self.database_path)
                
                return True
            
            return False
        
        except Exception as e:
            print('🤖 update error: ', e)
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
            data = load_json(path=self.database_path)
            
            if user_id in data:
                del data[user_id]
                to_json(data=data, path=self.database_path)
                
                return True
            
            return False
        except Exception as e:
            print('🤖 delete error: ', e)
            return False
