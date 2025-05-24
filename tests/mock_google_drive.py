from typing import List, Dict, Optional
import json
import os
from datetime import datetime, timedelta

class MockGoogleDriveService:
    """
    A mock implementation of Google Drive service for unit testing.
    Simulates file retrieval, listing, and metadata operations.
    """

    def __init__(self, mock_files: Optional[List[Dict]] = None):
        """
        Initialize the mock Google Drive service with optional mock files.
        
        :param mock_files: List of mock file dictionaries with metadata
        """
        self._files = mock_files or self._generate_default_mock_files()
    
    def _generate_default_mock_files(self) -> List[Dict]:
        """
        Generate a default set of mock files for testing.
        
        :return: List of mock file dictionaries
        """
        return [
            {
                "id": "file1",
                "name": "document1.txt",
                "mimeType": "text/plain",
                "createdTime": (datetime.now() - timedelta(days=5)).isoformat(),
                "modifiedTime": (datetime.now() - timedelta(days=2)).isoformat(),
                "size": "1024",
                "owners": [{"displayName": "Test User"}]
            },
            {
                "id": "file2",
                "name": "spreadsheet1.xlsx",
                "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "createdTime": (datetime.now() - timedelta(days=10)).isoformat(),
                "modifiedTime": (datetime.now() - timedelta(days=1)).isoformat(),
                "size": "2048",
                "owners": [{"displayName": "Test Admin"}]
            }
        ]
    
    def files(self):
        """
        Simulates the files().list() method of Google Drive API.
        
        :return: Self for method chaining
        """
        return self
    
    def execute(self):
        """
        Simulate API execution and return file list.
        
        :return: Dictionary with files and other metadata
        """
        return {"files": self._files}
    
    def get_file_metadata(self, file_id: str) -> Dict:
        """
        Retrieve metadata for a specific file.
        
        :param file_id: Unique identifier for the file
        :return: File metadata dictionary
        :raises FileNotFoundError: If file is not found
        """
        for file in self._files:
            if file["id"] == file_id:
                return file
        raise FileNotFoundError(f"File with ID {file_id} not found")
    
    def download_file(self, file_id: str) -> bytes:
        """
        Simulate file download.
        
        :param file_id: Unique identifier for the file
        :return: Simulated file content as bytes
        :raises FileNotFoundError: If file is not found
        """
        file_metadata = self.get_file_metadata(file_id)
        
        # Simulate different file content based on mime type
        if file_metadata["mimeType"] == "text/plain":
            return b"Sample text document content"
        elif "spreadsheet" in file_metadata["mimeType"]:
            return b"Sample spreadsheet content"
        
        return b""  # Default empty content