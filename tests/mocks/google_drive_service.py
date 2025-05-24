from typing import Dict, List, Optional, Any
import json
from datetime import datetime, timedelta

class MockGoogleDriveService:
    """
    A mock implementation of the Google Drive service for unit testing.
    Simulates core Google Drive API interactions without making actual API calls.
    """

    def __init__(self, mock_files: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the mock service with predefined files or an empty list.
        
        :param mock_files: List of file metadata dictionaries to simulate
        """
        self._files = mock_files or [
            {
                'id': 'file1',
                'name': 'sample_document.txt',
                'mimeType': 'text/plain',
                'createdTime': datetime.now().isoformat(),
                'modifiedTime': datetime.now().isoformat(),
                'size': '1024',
                'owners': [{'displayName': 'Test User'}],
                'content': 'This is a sample text document for testing.'
            },
            {
                'id': 'file2',
                'name': 'sample_spreadsheet.xlsx',
                'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'createdTime': (datetime.now() - timedelta(days=1)).isoformat(),
                'modifiedTime': (datetime.now() - timedelta(days=1)).isoformat(),
                'size': '2048',
                'owners': [{'displayName': 'Test User'}],
                'content': b'Mock Excel content'
            }
        ]

    def list_files(self, page_size: int = 100, query: Optional[str] = None) -> Dict[str, Any]:
        """
        Simulate listing files with optional filtering.
        
        :param page_size: Maximum number of files to return
        :param query: Optional query to filter files
        :return: Dictionary containing file metadata
        """
        if query:
            filtered_files = [
                file for file in self._files 
                if query.lower() in file['name'].lower()
            ]
        else:
            filtered_files = self._files

        return {
            'files': filtered_files[:page_size],
            'nextPageToken': None if len(filtered_files) <= page_size else 'mock_token'
        }

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Retrieve metadata for a specific file.
        
        :param file_id: ID of the file to retrieve
        :return: File metadata dictionary
        :raises ValueError: If file is not found
        """
        for file in self._files:
            if file['id'] == file_id:
                return file
        raise ValueError(f"File with ID {file_id} not found")

    def download_file(self, file_id: str) -> bytes:
        """
        Download file content by file ID.
        
        :param file_id: ID of the file to download
        :return: File content as bytes
        :raises ValueError: If file is not found
        """
        for file in self._files:
            if file['id'] == file_id:
                # Return content as bytes, handling different types
                content = file.get('content', b'')
                return content.encode('utf-8') if isinstance(content, str) else content
        
        raise ValueError(f"File with ID {file_id} not found")

    def add_mock_file(self, file_metadata: Dict[str, Any]) -> str:
        """
        Add a new mock file to the service.
        
        :param file_metadata: Metadata for the new file
        :return: ID of the newly added file
        """
        # Ensure file has required fields
        if 'id' not in file_metadata:
            file_metadata['id'] = f'mock_file_{len(self._files) + 1}'
        
        self._files.append(file_metadata)
        return file_metadata['id']