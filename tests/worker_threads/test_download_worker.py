import pytest
from unittest.mock import Mock, patch
import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from WorkerThreads.DownloadWorker import DownloadWorker

class MockGoogleDriveService:
    def __init__(self, files=None, error=None):
        self.files = files or []
        self.error = error

    def files(self):
        return self

    def list(self, **kwargs):
        if self.error:
            raise self.error
        return Mock(execute=lambda: {'files': self.files})

    def get(self, fileId):
        return Mock(execute=lambda: next((f for f in self.files if f['id'] == fileId), None))

def test_download_worker_initialization():
    """Test DownloadWorker initialization."""
    mock_service = MockGoogleDriveService()
    worker = DownloadWorker(mock_service)
    assert worker is not None
    assert worker.service == mock_service

def test_download_worker_file_retrieval():
    """Test file retrieval from Google Drive."""
    mock_files = [
        {
            'id': 'test_file_1', 
            'name': 'sample_document.txt', 
            'mimeType': 'text/plain'
        },
        {
            'id': 'test_file_2', 
            'name': 'sample_spreadsheet.xlsx', 
            'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
    ]
    mock_service = MockGoogleDriveService(files=mock_files)
    worker = DownloadWorker(mock_service)

    # Test file list retrieval
    retrieved_files = worker.list_files()
    assert len(retrieved_files) == 2
    assert all(file['id'] in ['test_file_1', 'test_file_2'] for file in retrieved_files)

def test_download_worker_error_handling():
    """Test error handling during file retrieval."""
    # Simulating an authentication error
    mock_auth_error = Exception("Authentication Failed")
    mock_service = MockGoogleDriveService(error=mock_auth_error)
    worker = DownloadWorker(mock_service)

    # Test error handling
    with pytest.raises(Exception, match="Authentication Failed"):
        worker.list_files()

def test_download_worker_file_filtering():
    """Test file filtering based on MIME types."""
    mock_files = [
        {
            'id': 'text_file', 
            'name': 'document.txt', 
            'mimeType': 'text/plain'
        },
        {
            'id': 'pdf_file', 
            'name': 'report.pdf', 
            'mimeType': 'application/pdf'
        },
        {
            'id': 'unsupported_file', 
            'name': 'image.png', 
            'mimeType': 'image/png'
        }
    ]
    mock_service = MockGoogleDriveService(files=mock_files)
    worker = DownloadWorker(mock_service)

    # Test supported file type filtering
    supported_files = worker.list_files()
    assert len(supported_files) == 2
    assert all(file['mimeType'] in ['text/plain', 'application/pdf'] for file in supported_files)

def test_download_worker_empty_drive():
    """Test behavior when Google Drive is empty."""
    mock_service = MockGoogleDriveService(files=[])
    worker = DownloadWorker(mock_service)

    # Test empty drive scenario
    retrieved_files = worker.list_files()
    assert len(retrieved_files) == 0