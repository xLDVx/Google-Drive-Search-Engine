import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid

@dataclass
class MockGDriveFile:
    """
    Represents a mock Google Drive file with essential metadata.
    """
    name: str
    mime_type: str
    created_time: datetime
    modified_time: datetime
    size: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parents: Optional[List[str]] = None
    content: Optional[bytes] = None

class MockGDriveService:
    """
    A mock implementation of Google Drive service for unit testing.
    Simulates file listing, retrieval, and metadata operations.
    """
    def __init__(self, mock_files: Optional[List[MockGDriveFile]] = None):
        """
        Initialize the mock service with optional predefined files.
        
        :param mock_files: List of MockGDriveFile to simulate existing files
        """
        self._files = mock_files or self._generate_default_files()
        self._file_dict = {file.id: file for file in self._files}

    def _generate_default_files(self) -> List[MockGDriveFile]:
        """
        Generate a set of default mock files for testing.
        
        :return: List of MockGDriveFile instances
        """
        base_time = datetime.now()
        default_files = [
            MockGDriveFile(
                id='file1_pdf',
                name='document1.pdf',
                mime_type='application/pdf',
                created_time=base_time - timedelta(days=10),
                modified_time=base_time - timedelta(days=5),
                size=1024 * 100,  # 100KB
                content=b'Sample PDF content for testing'
            ),
            MockGDriveFile(
                id='file2_docx',
                name='report.docx',
                mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                created_time=base_time - timedelta(days=15),
                modified_time=base_time - timedelta(days=2),
                size=1024 * 200,  # 200KB
                content=b'Sample Word document content'
            )
        ]
        return default_files

    def list_files(self, query: Optional[str] = None, 
                   page_size: int = 100, 
                   order_by: Optional[str] = None) -> List[MockGDriveFile]:
        """
        List files matching optional query with pagination and ordering.
        
        :param query: Optional search query to filter files
        :param page_size: Maximum number of files to return
        :param order_by: Optional ordering criteria
        :return: List of matching MockGDriveFile instances
        """
        if query:
            filtered_files = [
                file for file in self._files 
                if query.lower() in file.name.lower()
            ]
        else:
            filtered_files = self._files

        if order_by == 'createdTime':
            filtered_files.sort(key=lambda x: x.created_time)
        elif order_by == 'modifiedTime':
            filtered_files.sort(key=lambda x: x.modified_time)

        return filtered_files[:page_size]

    def get_file_metadata(self, file_id: str) -> Optional[MockGDriveFile]:
        """
        Retrieve file metadata by file ID.
        
        :param file_id: Unique identifier of the file
        :return: MockGDriveFile or None if not found
        """
        return self._file_dict.get(file_id)

    def download_file(self, file_id: str) -> Optional[bytes]:
        """
        Download file content by file ID.
        
        :param file_id: Unique identifier of the file
        :return: File content as bytes or None if file not found
        """
        file = self._file_dict.get(file_id)
        return file.content if file else None

    def create_file(self, file_data: MockGDriveFile) -> str:
        """
        Create a new mock file and add it to the service.
        
        :param file_data: MockGDriveFile to be added
        :return: ID of the created file
        """
        if not file_data.id:
            file_data.id = str(uuid.uuid4())
        
        self._files.append(file_data)
        self._file_dict[file_data.id] = file_data
        return file_data.id

    def delete_file(self, file_id: str) -> bool:
        """
        Delete a file from the mock service.
        
        :param file_id: Unique identifier of the file to delete
        :return: True if file was deleted, False otherwise
        """
        if file_id in self._file_dict:
            file_to_remove = self._file_dict[file_id]
            self._files.remove(file_to_remove)
            del self._file_dict[file_id]
            return True
        return False