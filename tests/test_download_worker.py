import os
import queue
import pytest
from unittest.mock import MagicMock, patch
from WorkerThreads.DownloadWorker import DownloadWorker

@pytest.fixture
def mock_credentials():
    """Create a mock credentials object."""
    mock_creds = MagicMock()
    mock_creds.authorize.return_value = MagicMock()
    return mock_creds

@pytest.fixture
def mock_queue():
    """Create a mock queue for testing."""
    return queue.Queue()

def test_valid_file_extensions():
    """Test that validFile method correctly identifies supported file extensions."""
    worker = DownloadWorker(queue.Queue(), MagicMock())
    
    # Test supported extensions
    supported_files = [
        "document.pdf", "image.jpg", "spreadsheet.xlsx", 
        "text.txt", "presentation.pptx", "data.csv"
    ]
    for file in supported_files:
        assert worker.validFile(file) is True, f"Failed for {file}"
    
    # Test unsupported extensions
    unsupported_files = [
        "script.py", "archive.zip", "executable.exe"
    ]
    for file in unsupported_files:
        assert worker.validFile(file) is False, f"Incorrectly passed for {file}"

@patch('WorkerThreads.DownloadWorker.discovery')
@patch('WorkerThreads.DownloadWorker.open')
@patch('WorkerThreads.DownloadWorker.MediaIoBaseDownload')
def test_download_file_success(mock_downloader, mock_open, mock_discovery, mock_credentials, mock_queue):
    """Test successful file download scenario."""
    # Setup mock objects
    mock_service = MagicMock()
    mock_media_request = MagicMock()
    mock_discovery.build.return_value = mock_service
    mock_service.files().get_media.return_value = mock_media_request
    
    # Mock downloader to simulate download progress
    mock_downloader_instance = MagicMock()
    mock_downloader_instance.next_chunk.return_value = (MagicMock(progress=lambda: 0.5), False)
    mock_downloader.return_value = mock_downloader_instance
    
    # Create DownloadWorker instance
    worker = DownloadWorker(mock_queue, mock_credentials)
    
    # Call download method
    worker.download_file("test_file_id", "test_file.pdf")
    
    # Assertions
    mock_discovery.build.assert_called_once()
    mock_service.files().get_media.assert_called_with(fileId="test_file_id")
    mock_downloader.assert_called_once()
    mock_downloader_instance.next_chunk.assert_called()

def test_invalid_file_not_downloaded(mock_queue, mock_credentials):
    """Ensure invalid files are not downloaded."""
    # Create a mock file dictionary with an unsupported extension
    mock_file = {
        "id": "test_file_id", 
        "name": "unsupported.xyz"
    }
    
    worker = DownloadWorker(mock_queue, mock_credentials)
    worker.download_file = MagicMock()  # Mock to prevent actual download
    
    # Manually simulate run method behavior
    if not os.path.exists(os.path.join("Data", "raw", mock_file["name"])) and worker.validFile(mock_file["name"]):
        worker.download_file(mock_file["id"], mock_file["name"])
    
    # Ensure download method was not called for invalid file
    worker.download_file.assert_not_called()

def test_download_worker_queue_handling(mock_queue, mock_credentials):
    """Test queue handling in DownloadWorker."""
    # Prepare mock files
    mock_files = [
        {"id": "file1", "name": "document1.pdf"},
        {"id": "file2", "name": "document2.txt"}
    ]
    
    # Populate queue
    for file in mock_files:
        mock_queue.put(file)
    
    # Create worker with mocked methods
    worker = DownloadWorker(mock_queue, mock_credentials)
    worker.validFile = MagicMock(return_value=True)
    worker.download_file = MagicMock()
    
    # Simulate worker run
    worker.run()
    
    # Verify downloads
    assert worker.download_file.call_count == len(mock_files)
    assert mock_queue.empty()