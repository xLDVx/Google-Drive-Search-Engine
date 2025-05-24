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
        return self

    def execute(self):
        return {"files": self.files}

@pytest.fixture
def mock_drive_service():
    """Fixture to create a mock Google Drive service."""
    return MockGoogleDriveService()

@pytest.fixture
def download_worker():
    """Fixture to create a DownloadWorker instance."""
    return DownloadWorker()

def test_download_worker_initialization():
    """Test that DownloadWorker can be initialized."""
    worker = DownloadWorker()
    assert worker is not None

@patch('WorkerThreads.DownloadWorker.build')
def test_list_files_in_drive(mock_build, mock_drive_service):
    """Test listing files from Google Drive."""
    # Prepare mock files
    mock_files = [
        {"id": "file1", "name": "document1.txt", "mimeType": "text/plain"},
        {"id": "file2", "name": "document2.pdf", "mimeType": "application/pdf"}
    ]
    mock_drive_service.files = mock_files
    mock_build.return_value.files.return_value.list.return_value.execute.return_value = {"files": mock_files}

    # Create DownloadWorker
    worker = DownloadWorker()

    # Mock the service build method
    worker.service = mock_build.return_value

    # List files
    files = worker.list_files()

    # Assertions
    assert len(files) == 2
    assert files[0]["name"] == "document1.txt"
    assert files[1]["name"] == "document2.pdf"

@patch('WorkerThreads.DownloadWorker.build')
def test_file_filtering_by_mime_type(mock_build, mock_drive_service):
    """Test filtering files by MIME type."""
    # Prepare mock files with different MIME types
    mock_files = [
        {"id": "file1", "name": "document1.txt", "mimeType": "text/plain"},
        {"id": "file2", "name": "document2.pdf", "mimeType": "application/pdf"},
        {"id": "file3", "name": "image.jpg", "mimeType": "image/jpeg"}
    ]
    mock_drive_service.files = mock_files
    mock_build.return_value.files.return_value.list.return_value.execute.return_value = {"files": mock_files}

    # Create DownloadWorker
    worker = DownloadWorker()
    worker.service = mock_build.return_value

    # Filter files by specific MIME types
    text_files = worker.list_files(mime_types=["text/plain"])
    pdf_files = worker.list_files(mime_types=["application/pdf"])

    # Assertions
    assert len(text_files) == 1
    assert text_files[0]["name"] == "document1.txt"
    assert len(pdf_files) == 1
    assert pdf_files[0]["name"] == "document2.pdf"

def test_handle_file_download_errors():
    """Test error handling during file download."""
    worker = DownloadWorker()
    
    # Test with invalid file
    with pytest.raises(ValueError):
        worker.download_file(None)
    
    # Test with missing file ID
    with pytest.raises(ValueError):
        worker.download_file({"name": "test.txt"})

@patch('WorkerThreads.DownloadWorker.build')
def test_file_download_functionality(mock_build):
    """Test basic file download functionality."""
    # Mock file details
    mock_file = {
        "id": "test_file_id", 
        "name": "test_document.txt", 
        "mimeType": "text/plain"
    }
    
    # Mock download method
    mock_media = Mock()
    mock_media.execute.return_value = b"Sample file content"
    mock_build.return_value.files.return_value.get_media.return_value = mock_media

    # Create DownloadWorker
    worker = DownloadWorker()
    worker.service = mock_build.return_value

    # Attempt download
    downloaded_content = worker.download_file(mock_file)

    # Assertions
    assert downloaded_content == b"Sample file content"