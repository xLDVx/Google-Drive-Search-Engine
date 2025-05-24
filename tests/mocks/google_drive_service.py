from typing import List, Dict, Optional, Any
import os
import mimetypes

class MockGoogleDriveService:
    """
    Mock implementation of Google Drive service for unit testing.
    Simulates file retrieval, metadata, and download operations.
    """
    def __init__(self, mock_files: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize mock Google Drive service with optional predefined files.
        
        :param mock_files: List of mock file dictionaries with metadata
        """
        self._files = mock_files or self._generate_default_mock_files()
    
    def _generate_default_mock_files(self) -> List[Dict[str, Any]]:
        """
        Generate a default set of mock files for testing.
        
        :return: List of mock file dictionaries
        """
        return [
            {
                'id': 'file1',
                'name': 'document1.txt',
                'mimeType': 'text/plain',
                'content': 'This is a sample text document for testing.',
                'webContentLink': 'https://example.com/file1.txt'
            },
            {
                'id': 'file2',
                'name': 'document2.pdf',
                'mimeType': 'application/pdf',
                'content': 'PDF content for testing text extraction.',
                'webContentLink': 'https://example.com/file2.pdf'
            }
        ]
    
    def list_files(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List files with optional filtering.
        
        :param query: Optional query to filter files
        :return: List of file metadata
        """
        if not query:
            return self._files
        
        return [
            file for file in self._files 
            if query.lower() in file['name'].lower()
        ]
    
    def get_file_metadata(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve file metadata by file ID.
        
        :param file_id: Unique identifier for the file
        :return: File metadata dictionary or None
        """
        return next((file for file in self._files if file['id'] == file_id), None)
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """
        Download file content by file ID.
        
        :param file_id: Unique identifier for the file
        :return: File content as bytes or None
        """
        file = self.get_file_metadata(file_id)
        return file['content'].encode('utf-8') if file else None
    
    def is_supported_file_type(self, mime_type: str) -> bool:
        """
        Check if the file type is supported for processing.
        
        :param mime_type: MIME type of the file
        :return: Boolean indicating file type support
        """
        supported_types = [
            'text/plain', 
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        return mime_type in supported_types