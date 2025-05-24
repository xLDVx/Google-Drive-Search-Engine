import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import queue

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

@patch('os.path.exists')
@patch('os.path.join')
def test_download_worker_initialization(mock_join, mock_exists, mock_que, mock_credentials):
    """Test that DownloadWorker can be initialized."""
    mock_exists.return_value = False
    mock_join.return_value = "/mock/path/to/file"
    
    worker = DownloadWorker(mock_que, mock_credentials)
    assert worker is not None

def test_valid_file():
    """Test file validation method."""
    worker = DownloadWorker(queue.Queue(), MagicMock())
    
    # Test supported file types
    assert worker.validFile("document.txt") == True
    assert worker.validFile("image.jpg") == True
    assert worker.validFile("spreadsheet.xlsx") == True
    
    # Test unsupported file types
    assert worker.validFile("script.sh") == False
    assert worker.validFile("data.dat") == False

@patch('WorkerThreads.DownloadWorker.discovery.build')
@patch('WorkerThreads.DownloadWorker.os.path.exists')
@patch('WorkerThreads.DownloadWorker.open', create=True)
def test_download_file(mock_open, mock_exists, mock_discovery_build, mock_que, mock_credentials):
    """Test file download functionality."""
    # Mock the dependencies
    mock_exists.return_value = False
    mock_file_service = MagicMock()
    mock_media_download = MagicMock()
    
    # Configure the mocks
    mock_discovery_build.return_value = mock_file_service
    mock_file_service.files.return_value.get_media.return_value = mock_media_download
    mock_media_download.next_chunk.return_value = (MagicMock(progress=lambda: 0.5), False)
    mock_media_download.next_chunk.side_effect = [
        (MagicMock(progress=lambda: 0.5), False), 
        (MagicMock(progress=lambda: 1.0), True)
    ]
    
    # Create DownloadWorker
    worker = DownloadWorker(mock_que, mock_credentials)
    
    # Perform file download
    worker.download_file("test_file_id", "test_file.txt")
    
    # Assertions
    mock_file_service.files.return_value.get_media.assert_called_once_with(fileId="test_file_id")
    assert mock_media_download.next_chunk.call_count == 2
    mock_open.assert_called_once_with(os.path.join("Data", "raw", "test_file.txt"), "wb")

def test_run_method(mock_que, mock_credentials):
    """Test the run method of DownloadWorker."""
    # Prepare a mock file
    mock_file = {
        "id": "test_file_id", 
        "name": "test_file.txt"
    }
    
    # Put mock file in queue
    mock_que.put(mock_file)
    
    # Create worker
    with patch.object(DownloadWorker, 'download_file') as mock_download, \
         patch.object(DownloadWorker, 'validFile', return_value=True), \
         patch('os.path.exists', return_value=False):
        
        worker = DownloadWorker(mock_que, mock_credentials)
        worker.run()
        
        # Verify download method was called
        mock_download.assert_called_once_with(mock_file["id"], mock_file["name"])
        # Verify task is marked as done
        assert mock_que.empty()