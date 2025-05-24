import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock, call
import queue
import io

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WorkerThreads.DownloadWorker import DownloadWorker
from googleapiclient import discovery

@pytest.fixture
def mock_que():
    """Fixture to create a mock queue."""
    return queue.Queue()

@pytest.fixture
def mock_credentials():
    """Fixture to create mock credentials."""
    mock_creds = MagicMock()
    mock_creds.authorize.return_value = MagicMock()
    return mock_creds

def test_download_worker_initialization(mock_que, mock_credentials):
    """Test that DownloadWorker can be initialized."""
    worker = DownloadWorker(mock_que, mock_credentials)
    assert worker is not None
    assert worker.que == mock_que
    assert worker.credentials == mock_credentials

def test_valid_file():
    """Test file validation method."""
    worker = DownloadWorker(queue.Queue(), MagicMock())
    
    # Test supported file types
    supported_files = [
        "document.txt", "image.jpg", "spreadsheet.xlsx", 
        "presentation.pptx", "pdf.pdf", "audio.mp3"
    ]
    unsupported_files = [
        "script.sh", "data.dat", "executable.exe", 
        "compressed.zip", "archive.tar"
    ]
    
    for file in supported_files:
        assert worker.validFile(file) == True, f"Failed for supported file: {file}"
    
    for file in unsupported_files:
        assert worker.validFile(file) == False, f"Failed for unsupported file: {file}"

@patch('WorkerThreads.DownloadWorker.os.path.join', return_value='/Data/raw/test_file.txt')
@patch('WorkerThreads.DownloadWorker.os.makedirs')
@patch('WorkerThreads.DownloadWorker.discovery.build')
@patch('WorkerThreads.DownloadWorker.open', create=True)
def test_download_file_successful(mock_open, mock_discovery_build, mock_makedirs, mock_join, mock_que, mock_credentials):
    """Test successful file download functionality."""
    # Prepare mock objects
    mock_service = MagicMock()
    mock_request = MagicMock()
    mock_downloader = MagicMock()
    
    # Configure mocks
    mock_discovery_build.return_value = mock_service
    mock_service.files.return_value.get_media.return_value = mock_request
    
    mock_status = MagicMock()
    mock_status.progress.return_value = 0.5
    mock_downloader.next_chunk.side_effect = [
        (mock_status, False),
        (mock_status, True)
    ]
    
    # Patch MediaIoBaseDownload to return our mock downloader
    with patch('WorkerThreads.DownloadWorker.MediaIoBaseDownload', return_value=mock_downloader):
        # Create DownloadWorker
        worker = DownloadWorker(mock_que, mock_credentials)
        
        # Perform file download
        result = worker.download_file("test_file_id", "test_file.txt")
    
    # Assertions
    assert result == True
    mock_service.files.return_value.get_media.assert_called_once_with(fileId="test_file_id")
    mock_open.assert_called_once_with('/Data/raw/test_file.txt', 'wb')
    assert mock_downloader.next_chunk.call_count == 2

def test_download_file_error_scenarios(mock_que, mock_credentials):
    """Test various error scenarios during file download."""
    worker = DownloadWorker(mock_que, mock_credentials)
    
    # Test invalid input scenarios
    error_test_cases = [
        (None, None, ValueError, "Invalid file ID"),
        (None, "test.txt", ValueError, "Invalid file ID"),
        ("", "test.txt", ValueError, "Invalid file ID")
    ]
    
    for file_id, file_name, expected_exception, error_message in error_test_cases:
        with pytest.raises(expected_exception, match=error_message):
            worker.download_file(file_id, file_name)

@patch('WorkerThreads.DownloadWorker.discovery.build')
def test_download_file_network_error(mock_discovery_build, mock_que, mock_credentials, caplog):
    """Test handling of network or service-related errors."""
    # Configure mock to raise an exception
    mock_service = MagicMock()
    mock_service.files.return_value.get_media.side_effect = Exception("Network error")
    mock_discovery_build.return_value = mock_service
    
    worker = DownloadWorker(mock_que, mock_credentials)
    
    # Use a mock file for testing
    mock_file = {
        "id": "test_file_id", 
        "name": "test_file.txt"
    }
    
    # Expect an exception to be raised
    with pytest.raises(Exception, match="Network error"):
        worker.download_file(mock_file["id"], mock_file["name"])
    
    # Verify logging
    assert "Download failed for test_file.txt" in caplog.text

def test_run_method_error_handling(mock_que, mock_credentials, caplog):
    """Test error handling in the run method."""
    # Prepare a mock file
    mock_file = {
        "id": "test_file_id", 
        "name": "test_file.txt"
    }
    
    # Put mock file in queue
    mock_que.put(mock_file)
    
    # Create worker
    with patch.object(DownloadWorker, 'download_file', side_effect=Exception("Download failed")) as mock_download, \
         patch.object(DownloadWorker, 'validFile', return_value=True), \
         patch('os.path.exists', return_value=False):
        
        worker = DownloadWorker(mock_que, mock_credentials)
        worker.run()
        
        # Verify download method was called
        mock_download.assert_called_once_with(mock_file["id"], mock_file["name"])
        
        # Verify error was logged
        assert "Download failed for test_file.txt" in caplog.text
        
        # Verify task is marked as done
        assert mock_que.empty()