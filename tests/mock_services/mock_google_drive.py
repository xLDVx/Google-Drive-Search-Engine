from typing import List, Dict, Optional
import os
import mimetypes
from dataclasses import dataclass, field

@dataclass
class MockGoogleDriveFile:
    """Simulate a Google Drive file with core attributes."""
    id: str
    name: str
    mime_type: str
    parents: List[str] = field(default_factory=list)
    content: Optional[bytes] = None
    size: int = 0

class MockGoogleDriveService:
    """Mock implementation of Google Drive service for unit testing."""
    
    def __init__(self, mock_files: Optional[List[MockGoogleDriveFile]] = None):
        """
        Initialize mock service with predefined or empty file collection.
        
        :param mock_files: Optional list of predefined mock files
        """
        self._files = mock_files or []
        self._file_map = {file.id: file for file in self._files}
    
    def list_files(self, query: Optional[str] = None) -> List[MockGoogleDriveFile]:
        """
        List files with optional filtering.
        
        :param query: Optional query to filter files
        :return: List of matching files
        """
        if not query:
            return self._files
        
        return [
            file for file in self._files 
            if query.lower() in file.name.lower() or query.lower() in str(file.mime_type).lower()
        ]
    
    def get_file_metadata(self, file_id: str) -> Optional[MockGoogleDriveFile]:
        """
        Retrieve file metadata by ID.
        
        :param file_id: Unique file identifier
        :return: File metadata or None
        """
        return self._file_map.get(file_id)
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """
        Download file content by ID.
        
        :param file_id: Unique file identifier
        :return: File content as bytes or None
        """
        file = self._file_map.get(file_id)
        return file.content if file else None
    
    def add_mock_file(self, file: MockGoogleDriveFile):
        """
        Add a mock file to the service.
        
        :param file: MockGoogleDriveFile to add
        """
        self._files.append(file)
        self._file_map[file.id] = file
    
    def create_file_from_local(self, local_path: str) -> MockGoogleDriveFile:
        """
        Create a mock file from a local file.
        
        :param local_path: Path to local file
        :return: Created MockGoogleDriveFile
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")
        
        with open(local_path, 'rb') as f:
            content = f.read()
        
        # More precise mime type detection
        mime_type, _ = mimetypes.guess_type(local_path)
        if mime_type is None:
            with open(local_path, 'r', encoding='utf-8') as f:
                sample = f.read(1024)
                mime_type = 'text/plain' if sample.isprintable() else 'application/octet-stream'
        
        mock_file = MockGoogleDriveFile(
            id=str(len(self._files) + 1),
            name=os.path.basename(local_path),
            mime_type=mime_type or 'application/octet-stream',
            content=content,
            size=len(content)
        )
        
        self.add_mock_file(mock_file)
        return mock_file