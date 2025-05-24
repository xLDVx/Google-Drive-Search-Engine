import json
import os
from typing import Dict, Optional

class AuthenticationManager:
    """
    Manages authentication credentials and token management for Google Drive API.
    """
    def __init__(self, client_id_path: str = '.auth/client_id.json', 
                 credentials_path: str = '.auth/credentials.json'):
        """
        Initialize the authentication manager with paths to credentials.

        Args:
            client_id_path (str): Path to client ID configuration file
            credentials_path (str): Path to stored credentials file
        """
        self.client_id_path = client_id_path
        self.credentials_path = credentials_path

    def get_client_id(self) -> Optional[Dict[str, str]]:
        """
        Retrieve client ID configuration.

        Returns:
            Optional[Dict[str, str]]: Client ID configuration or None if not found
        """
        try:
            with open(self.client_id_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            raise ValueError("Invalid client ID JSON configuration")

    def get_credentials(self) -> Optional[Dict[str, str]]:
        """
        Retrieve stored credentials.

        Returns:
            Optional[Dict[str, str]]: Stored credentials or None if not found
        """
        try:
            with open(self.credentials_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            raise ValueError("Invalid credentials JSON configuration")

    def is_token_valid(self) -> bool:
        """
        Check if the current token is valid.

        Returns:
            bool: Whether the token is valid
        """
        credentials = self.get_credentials()
        return credentials is not None and 'access_token' in credentials