from typing import List, Dict, Any, Optional
import os
import json
from datetime import datetime, timedelta

class MockGoogleDriveService:
    """
    A mock implementation of Google Drive service for unit testing.
    Simulates file retrieval, listing, and metadata operations.
    """
    
    def __init__(self, mock_files: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the mock Google Drive service with optional predefined files.
        
        :param mock_files: List of mock file dictionaries
        """
        self._mock_files = mock_files or self._generate_default_mock_files()
    
    def _generate_default_mock_files(self) -> List[Dict[str, Any]]:
        """
        Generate a set of default mock files for testing.
        
        :return: List of mock file dictionaries
        """
        return [
            {
                'id': 'file1',
                'name': 'document1.txt',
                'mimeType': 'text/plain',
                'size': 1024,
                'createdTime': (datetime.now() - timedelta(days=1)).isoformat(),
                'content': 'Sample text content for document1'
            },
            {
                'id': 'file2',
                'name': 'spreadsheet1.xlsx',
                'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'size': 2048,
                'createdTime': (datetime.now() - timedelta(days=2)).isoformat(),
                'content': 'Mock spreadsheet content'
            },
            {
                'id': 'file3',
                'name': 'presentation1.pptx',
                'mimeType': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'size': 3072,
                'createdTime': (datetime.now() - timedelta(days=3)).isoformat(),
                'content': 'Mock presentation content'
            }
        ]
    
    def list_files(self, page_size: int = 100, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List files in the mock Google Drive.
        
        :param page_size: Maximum number of files to return
        :param query: Optional query to filter files
        :return: List of file metadata
        """
        files = self._mock_files[:page_size]
        
        if query:
            files = [
                file for file in files 
                if query.lower() in file['name'].lower()
            ]
        
        return files
    
    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Retrieve metadata for a specific file.
        
        :param file_id: ID of the file to retrieve
        :return: File metadata dictionary
        :raises FileNotFoundError: If file is not found
        """
        for file in self._mock_files:
            if file['id'] == file_id:
                return file
        
        raise FileNotFoundError(f"File with ID {file_id} not found")
    
    def download_file(self, file_id: str) -> str:
        """
        Download file content by file ID.
        
        :param file_id: ID of the file to download
        :return: File content as string
        :raises FileNotFoundError: If file is not found
        """
        metadata = self.get_file_metadata(file_id)
        return metadata.get('content', '')