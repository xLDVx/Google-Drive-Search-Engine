from typing import Dict, List, Optional, Any
import json
import os
from datetime import datetime

class MockGDriveService:
    """
    A mock Google Drive service for unit testing document search and extraction functionality.
    Simulates file retrieval, metadata, and content generation without actual API calls.
    """

    def __init__(self, mock_files: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the mock Google Drive service with optional predefined mock files.

        :param mock_files: List of mock file dictionaries with metadata and content
        """
        self.mock_files = mock_files or self._generate_default_mock_files()

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
                'content': 'This is a sample text document about machine learning.',
                'modifiedTime': datetime.now().isoformat()
            },
            {
                'id': 'file2',
                'name': 'document2.pdf',
                'mimeType': 'application/pdf',
                'content': 'Artificial Intelligence is transforming various industries.',
                'modifiedTime': datetime.now().isoformat()
            },
            {
                'id': 'file3',
                'name': 'document3.docx',
                'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'content': 'Data science requires strong mathematical and programming skills.',
                'modifiedTime': datetime.now().isoformat()
            }
        ]

    def list_files(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List files from the mock Google Drive, optionally filtered by a query.

        :param query: Optional query to filter files
        :return: List of file metadata
        """
        if not query:
            return self.mock_files

        return [
            file for file in self.mock_files
            if query.lower() in file['name'].lower() or query.lower() in file['content'].lower()
        ]

    def get_file_content(self, file_id: str) -> Optional[str]:
        """
        Retrieve file content by file ID.

        :param file_id: ID of the file to retrieve
        :return: File content or None if file not found
        """
        for file in self.mock_files:
            if file['id'] == file_id:
                return file['content']
        return None

    def get_file_metadata(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve file metadata by file ID.

        :param file_id: ID of the file to retrieve metadata for
        :return: File metadata or None if file not found
        """
        for file in self.mock_files:
            if file['id'] == file_id:
                return {k: v for k, v in file.items() if k != 'content'}
        return None

    def download_file(self, file_id: str, save_path: str) -> bool:
        """
        Download a mock file to a specified path.

        :param file_id: ID of the file to download
        :param save_path: Path to save the downloaded file
        :return: True if successful, False otherwise
        """
        content = self.get_file_content(file_id)
        if content is None:
            return False

        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False