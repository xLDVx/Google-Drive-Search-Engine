from typing import List, Dict, Optional, Any
import json
import os
from datetime import datetime, timedelta

class MockGoogleDriveService:
    """
    A mock implementation of Google Drive service for unit testing.
    
    This service simulates Google Drive API interactions without making actual 
    network calls, allowing for predictable and controllable testing scenarios.
    """
    
    def __init__(self, mock_files: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the mock Google Drive service with optional predefined files.
        
        :param mock_files: List of file dictionaries to simulate in the mock service
        """
        # Default mock files if none are provided
        self._files = mock_files or [
            {
                'id': 'file1',
                'name': 'document1.txt',
                'mimeType': 'text/plain',
                'content': 'This is the content of document1.',
                'createdTime': (datetime.now() - timedelta(days=1)).isoformat(),
            },
            {
                'id': 'file2',
                'name': 'document2.pdf',
                'mimeType': 'application/pdf',
                'content': 'PDF content for document2.',
                'createdTime': (datetime.now() - timedelta(days=2)).isoformat(),
            }
        ]
    
    def list_files(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List files in the mock Google Drive, optionally filtered by query.
        
        :param query: Optional query to filter files
        :return: List of file metadata
        """
        if not query:
            return self._files
        
        # Simple query filtering
        return [
            file for file in self._files 
            if query.lower() in file['name'].lower()
        ]
    
    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Retrieve metadata for a specific file.
        
        :param file_id: ID of the file to retrieve
        :return: File metadata dictionary
        :raises FileNotFoundError: If file is not found
        """
        for file in self._files:
            if file['id'] == file_id:
                return file
        raise FileNotFoundError(f"File with ID {file_id} not found")
    
    def download_file(self, file_id: str) -> bytes:
        """
        Download file content by file ID.
        
        :param file_id: ID of the file to download
        :return: File content as bytes
        :raises FileNotFoundError: If file is not found
        """
        for file in self._files:
            if file['id'] == file_id:
                return file['content'].encode('utf-8')
        raise FileNotFoundError(f"File with ID {file_id} not found")
    
    def add_file(self, file_data: Dict[str, Any]) -> str:
        """
        Add a new file to the mock service.
        
        :param file_data: Dictionary containing file metadata and content
        :return: ID of the newly added file
        """
        # Ensure required fields are present
        if 'name' not in file_data or 'content' not in file_data:
            raise ValueError("File must have 'name' and 'content' fields")
        
        # Generate a unique ID
        file_data['id'] = f"file_{len(self._files) + 1}"
        file_data['createdTime'] = datetime.now().isoformat()
        
        self._files.append(file_data)
        return file_data['id']