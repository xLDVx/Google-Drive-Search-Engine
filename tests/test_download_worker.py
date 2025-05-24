import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WorkerThreads.DownloadWorker import DownloadWorker

class MockGoogleDriveService:
    def __init__(self, files=None):
        self.files = files or []

    def files(self):
        return self

    def list(self, **kwargs):
        return Mock(execute=lambda: {'files': self.files})

    def get(self, fileId):
        return Mock(execute=lambda: next((f for f in self.files if f['id'] == fileId), None))

def test_download_worker_initialization():
    """Test DownloadWorker initialization."""
    worker = DownloadWorker()
    assert worker is not None

@patch('WorkerThreads.DownloadWorker.build')
def test_google_drive_file_retrieval(mock_build):
    """Test Google Drive file retrieval logic."""
    # Mock files to simulate Google Drive contents
    mock_files = [
        {'id': 'file1', 'name': 'document1.txt', 'mimeType': 'text/plain'},
        {'id': 'file2', 'name': 'document2.pdf', 'mimeType': 'application/pdf'}
    ]
    
    # Create mock Google Drive service
    mock_service = MockGoogleDriveService(files=mock_files)
    mock_build.return_value = mock_service

    # Initialize DownloadWorker
    worker = DownloadWorker()
    
    # Test file listing
    files = worker.list_files()
    assert len(files) == 2
    assert all('id' in file and 'name' in file for file in files)

def test_file_download_error_handling():
    """Test error handling during file download."""
    worker = DownloadWorker()
    
    # Simulate file download with non-existent file
    with pytest.raises(FileNotFoundError):
        worker.download_file('non_existent_file_id')

@patch('WorkerThreads.DownloadWorker.build')
def test_file_type_filtering(mock_build):
    """Test filtering of file types during retrieval."""
    mock_files = [
        {'id': 'txt1', 'name': 'text.txt', 'mimeType': 'text/plain'},
        {'id': 'pdf1', 'name': 'document.pdf', 'mimeType': 'application/pdf'},
        {'id': 'doc1', 'name': 'image.jpg', 'mimeType': 'image/jpeg'}
    ]
    
    mock_service = MockGoogleDriveService(files=mock_files)
    mock_build.return_value = mock_service

    worker = DownloadWorker()
    
    # Test file type filtering
    text_files = worker.list_files(mime_types=['text/plain'])
    assert len(text_files) == 1
    assert text_files[0]['name'] == 'text.txt'

def test_authentication_dependency():
    """Test that DownloadWorker requires authentication."""
    worker = DownloadWorker()
    
    # Simulate lack of credentials
    with pytest.raises(PermissionError):
        worker.authenticate()