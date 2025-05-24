import pytest
from unittest.mock import Mock, patch
import queue
import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from WorkerThreads.DownloadWorker import DownloadWorker
from oauth2client.client import OAuth2Credentials

def create_mock_credentials():
    """Create a mock OAuth2Credentials instance."""
    mock_creds = Mock(spec=OAuth2Credentials)
    mock_creds.access_token = 'mock_access_token'
    mock_creds.authorize.return_value = Mock()
    return mock_creds

def test_download_worker_initialization():
    """Test DownloadWorker initialization."""
    mock_queue = queue.Queue()
    mock_credentials = create_mock_credentials()
    worker = DownloadWorker(mock_queue, mock_credentials)
    assert worker is not None
    assert worker.que == mock_queue
    assert worker.credentials == mock_credentials

def test_download_worker_valid_file_extensions():
    """Test file extension validation."""
    mock_queue = queue.Queue()
    mock_credentials = create_mock_credentials()
    worker = DownloadWorker(mock_queue, mock_credentials)

    # Test supported file extensions
    supported_files = [
        "document.txt", 
        "report.pdf", 
        "spreadsheet.xlsx", 
        "image.jpg", 
        "data.csv"
    ]
    unsupported_files = [
        "document.exe", 
        "script.bat", 
        "malware.zip"
    ]

    for file in supported_files:
        assert worker.validFile(file) is True, f"Failed for supported file: {file}"

    for file in unsupported_files:
        assert worker.validFile(file) is False, f"Failed for unsupported file: {file}"

def test_download_worker_file_download_error_handling(monkeypatch):
    """Test error handling during file download."""
    mock_queue = queue.Queue()
    mock_credentials = create_mock_credentials()
    worker = DownloadWorker(mock_queue, mock_credentials)

    # Mocking the download_file method to raise an exception
    def mock_download_file(self, file_id, output_file):
        raise Exception("Download Error")

    monkeypatch.setattr(worker, 'download_file', mock_download_file)

    # Simulate a file to download
    test_file = {"id": "test_file_id", "name": "test_file.txt"}
    mock_queue.put(test_file)

    # Capture print output to check error handling
    with patch('builtins.print') as mock_print:
        worker.run()
        mock_print.assert_any_call("Download Error")

def test_download_worker_queue_empty_handling():
    """Test worker behavior when queue is empty."""
    mock_queue = queue.Queue()
    mock_credentials = create_mock_credentials()
    worker = DownloadWorker(mock_queue, mock_credentials)

    # The worker should exit when queue is empty
    worker.run()