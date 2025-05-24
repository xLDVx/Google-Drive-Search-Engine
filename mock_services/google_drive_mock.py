from typing import Dict, List, Optional, Any
import os
import json
import random
import mimetypes
from datetime import datetime, timedelta

class MockGoogleDriveService:
    """
    A mock implementation of Google Drive service for unit testing.
    Simulates file retrieval, metadata, and download capabilities.
    """

    def __init__(self, mock_files: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the mock Google Drive service with predefined or generated mock files.
        
        :param mock_files: Optional list of mock file dictionaries to use
        """
        self.mock_files = mock_files or self._generate_mock_files()

    def _generate_mock_files(self, num_files: int = 10) -> List[Dict[str, Any]]:
        """
        Generate a list of mock files with realistic attributes.
        
        :param num_files: Number of mock files to generate
        :return: List of mock file dictionaries
        """
        file_types = [
            '.txt', '.pdf', '.docx', '.xlsx', '.pptx', 
            '.csv', '.md', '.json', '.html'
        ]
        mock_files = []

        for i in range(num_files):
            file_type = random.choice(file_types)
            file_name = f"mock_document_{i}{file_type}"
            
            mock_file = {
                'id': f"file_{i}_mock_id",
                'name': file_name,
                'mimeType': mimetypes.guess_type(file_name)[0] or 'application/octet-stream',
                'createdTime': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                'modifiedTime': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                'size': random.randint(100, 10000),
                'content': f"Mock content for {file_name}"
            }
            mock_files.append(mock_file)

        return mock_files

    def list_files(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List files, optionally filtered by a query.
        
        :param query: Optional query to filter files
        :return: List of file metadata
        """
        if not query:
            return self.mock_files

        filtered_files = [
            file for file in self.mock_files 
            if query.lower() in file['name'].lower()
        ]
        return filtered_files

    def get_file_metadata(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata for a specific file.
        
        :param file_id: ID of the file to retrieve
        :return: File metadata or None if not found
        """
        return next((file for file in self.mock_files if file['id'] == file_id), None)

    def download_file(self, file_id: str) -> Optional[bytes]:
        """
        Download a file's content by its ID.
        
        :param file_id: ID of the file to download
        :return: File content as bytes, or None if file not found
        """
        file_metadata = self.get_file_metadata(file_id)
        
        if not file_metadata:
            return None
        
        return file_metadata.get('content', '').encode('utf-8')

    def export_file(self, file_id: str, mime_type: str) -> Optional[bytes]:
        """
        Export a file in a specific MIME type.
        
        :param file_id: ID of the file to export
        :param mime_type: Desired export MIME type
        :return: Exported file content as bytes, or None if file not found
        """
        file_metadata = self.get_file_metadata(file_id)
        
        if not file_metadata:
            return None
        
        # In a real implementation, this would handle different export formats
        return file_metadata.get('content', '').encode('utf-8')