from typing import Dict, List, Optional, Any
import os
import json
import mimetypes

class MockGoogleDriveService:
    """
    A mock implementation of Google Drive service for unit testing.
    Simulates Google Drive API interactions without making actual external calls.
    """
    
    def __init__(self, mock_files_directory: str = 'tests/mocks/sample_files'):
        """
        Initialize the mock Google Drive service.
        
        :param mock_files_directory: Directory containing mock files for testing
        """
        self.mock_files_directory = mock_files_directory
        self._create_sample_files_directory()
    
    def _create_sample_files_directory(self):
        """
        Ensure the mock files directory exists.
        """
        os.makedirs(self.mock_files_directory, exist_ok=True)
    
    def list_files(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List files in the mock Google Drive, with optional filtering.
        
        :param query: Optional query to filter files
        :return: List of file metadata dictionaries
        """
        files = []
        for filename in os.listdir(self.mock_files_directory):
            file_path = os.path.join(self.mock_files_directory, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Create file metadata
            file_metadata = {
                'id': filename,
                'name': filename,
                'mimeType': mimetypes.guess_type(filename)[0] or 'application/octet-stream',
                'size': os.path.getsize(file_path)
            }
            
            # Apply optional query filtering
            if query is None or self._matches_query(file_metadata, query):
                files.append(file_metadata)
        
        return files
    
    def _matches_query(self, file_metadata: Dict[str, Any], query: str) -> bool:
        """
        Check if a file matches the given query.
        
        :param file_metadata: File metadata dictionary
        :param query: Search query
        :return: True if file matches query, False otherwise
        """
        # Simple query matching (case-insensitive)
        query = query.lower()
        return (
            query in file_metadata['name'].lower() or 
            query in (file_metadata.get('mimeType', '') or '').lower()
        )
    
    def download_file(self, file_id: str) -> bytes:
        """
        Download a file from the mock Google Drive.
        
        :param file_id: ID of the file to download
        :return: File contents as bytes
        :raises FileNotFoundError: If file does not exist
        """
        file_path = os.path.join(self.mock_files_directory, file_id)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File with ID {file_id} not found")
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    def create_sample_files(self, files_data: List[Dict[str, str]]):
        """
        Create sample files for testing purposes.
        
        :param files_data: List of file data dictionaries with 'name' and 'content'
        """
        for file_info in files_data:
            file_path = os.path.join(self.mock_files_directory, file_info['name'])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_info['content'])