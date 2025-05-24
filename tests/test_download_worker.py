import pytest
import os
import sys
import queue
from unittest.mock import Mock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WorkerThreads.DownloadWorker import DownloadWorker

class MockCredentials:
    def __init__(self):
        self.token = 'mock_token'
    
    def authorize(self, http_obj):
        return http_obj

class MockDiscoveryService:
    def __init__(self, files=None):
        self.files = files or []
        self.downloaded_files = []

    def files(self):
        return self

    def get_media(self, fileId):
        return f"media_request_{fileId}"

    def get(self, fileId):
        return next((f for f in self.files if f['id'] == fileId), None)

def test_download_worker_initialization():
    """Test DownloadWorker initialization."""
    mock_queue = queue.Queue()
    mock_credentials = MockCredentials()
    worker = DownloadWorker(mock_queue, mock_credentials)
    assert worker is not None

def test_valid_file_extension():
    """Test file extension validation."""
    mock_queue = queue.Queue()
    mock_credentials = MockCredentials()
    worker = DownloadWorker(mock_queue, mock_credentials)
    
    valid_files = [
        'document.txt', 
        'image.jpg', 
        'spreadsheet.xlsx', 
        'presentation.pptx'
    ]
    invalid_files = [
        'document.xyz', 
        'video.mp4', 
        'script.py'
    ]
    
    for file in valid_files:
        assert worker.validFile(file) is True
    
    for file in invalid_files:
        assert worker.validFile(file) is False

@patch('WorkerThreads.DownloadWorker.discovery.build')
def test_file_download(mock_discovery_build):
    """Test file download process."""
    mock_queue = queue.Queue()
    mock_credentials = MockCredentials()
    
    # Prepare test data
    test_file = {
        'id': 'test_file_id', 
        'name': 'test_document.txt'
    }
    mock_queue.put(test_file)
    
    # Create a mock discovery service
    mock_service = MockDiscoveryService(files=[test_file])
    mock_discovery_build.return_value = mock_service
    
    # Create worker
    worker = DownloadWorker(mock_queue, mock_credentials)
    
    # Ensure Data/raw directory exists
    os.makedirs('Data/raw', exist_ok=True)
    
    # Patch os.path.exists to simulate file not existing
    with patch('os.path.exists', return_value=False):
        # Patch open to prevent actual file writing
        with patch('builtins.open', create=True) as mock_open:
            worker.run()
    
    # Verify
    assert mock_queue.empty()

def test_supported_file_extensions():
    """Test the list of supported file extensions."""
    mock_queue = queue.Queue()
    mock_credentials = MockCredentials()
    worker = DownloadWorker(mock_queue, mock_credentials)
    
    # This assumes the method remains the same as in the actual implementation
    supported_extensions = [
        ".csv", ".doc", ".docx", ".epub", ".eml", ".gif", ".jpg", ".jpeg", 
        ".json", ".html", ".htm", ".mp3", ".msg", ".odt", ".ogg", ".pdf", 
        ".png", ".pptx", ".ps", ".rtf", ".tiff", ".tif", ".txt", ".wav", 
        ".xlsx", ".xls"
    ]
    
    # Test each supported extension
    for ext in supported_extensions:
        assert worker.validFile(f"test_file{ext}") is True