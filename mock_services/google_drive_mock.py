from typing import Dict, List, Optional, Any
import os
import json
from datetime import datetime, timedelta

class MockGoogleDriveService:
    """
    A mock implementation of Google Drive service for unit testing.
    Simulates Drive API interactions without making external calls.
    """
    
    def __init__(self, mock_files: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the mock Google Drive service with optional predefined files.
        
        :param mock_files: List of mock file dictionaries with metadata
        """
        self._mock_files = mock_files or self._generate_default_mock_files()
        self._file_contents = {}
    
    def _generate_default_mock_files(self) -> List[Dict[str, Any]]:
        """
        Generate a default set of mock files for testing.
        
        :return: List of mock file metadata
        """
        return [
            {
                'id': 'file1',
                'name': 'document1.txt',
                'mimeType': 'text/plain',
                'createdTime': (datetime.now() - timedelta(days=1)).isoformat(),
                'size': '1024'
            },
            {
                'id': 'file2',
                'name': 'spreadsheet1.xlsx',
                'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'createdTime': (datetime.now() - timedelta(days=2)).isoformat(),
                'size': '2048'
            }
        ]
    
    def files(self) -> 'MockFilesList':
        """
        Simulate the files().list() method of Google Drive service.
        
        :return: MockFilesList instance for method chaining
        """
        return MockFilesList(self._mock_files)
    
    def files_get(self, file_id: str, media_mime_type: Optional[str] = None) -> 'MockFile':
        """
        Simulate the files().get() method for retrieving file metadata.
        
        :param file_id: ID of the file to retrieve
        :param media_mime_type: Optional mime type for media retrieval
        :return: MockFile instance
        """
        for file in self._mock_files:
            if file['id'] == file_id:
                return MockFile(file)
        raise FileNotFoundError(f"File with ID {file_id} not found")
    
    def set_file_content(self, file_id: str, content: str):
        """
        Set content for a mock file to simulate file download.
        
        :param file_id: ID of the file
        :param content: Content to set for the file
        """
        self._file_contents[file_id] = content
    
    def download_file(self, file_id: str) -> bytes:
        """
        Simulate file download.
        
        :param file_id: ID of the file to download
        :return: File content as bytes
        """
        content = self._file_contents.get(file_id)
        if content is None:
            raise FileNotFoundError(f"No content found for file ID {file_id}")
        return content.encode('utf-8')

class MockFilesList:
    """Helper class to simulate files().list() method chaining."""
    
    def __init__(self, files: List[Dict[str, Any]]):
        """
        Initialize MockFilesList with a list of files.
        
        :param files: List of file metadata dictionaries
        """
        self._files = files
    
    def execute(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Simulate execute() method of files().list().
        
        :return: Dictionary with 'files' key containing file metadata
        """
        return {'files': self._files}

class MockFile:
    """Helper class to simulate individual file metadata retrieval."""
    
    def __init__(self, file_metadata: Dict[str, Any]):
        """
        Initialize MockFile with file metadata.
        
        :param file_metadata: Dictionary containing file metadata
        """
        self._metadata = file_metadata
    
    def execute(self) -> Dict[str, Any]:
        """
        Simulate execute() method for file metadata.
        
        :return: File metadata dictionary
        """
        return self._metadata