import os
import queue
import pytest
from unittest.mock import Mock, patch, mock_open
from WorkerThreads.DownloadWorker import DownloadWorker

class MockCredentials:
    def authorize(self, http):
        return http

class TestDownloadWorker:
    @pytest.fixture
    def mock_queue(self):
        """Create a mock queue for testing."""
        return queue.Queue()

    @pytest.fixture
    def mock_credentials(self):
        """Create mock credentials."""
        return MockCredentials()

    def test_valid_file_extensions(self):
        """Test valid file extensions are correctly identified."""
        worker = DownloadWorker(queue.Queue(), None)
        
        # Test supported extensions
        supported_files = [
            "document.pdf", "data.csv", "image.jpg", 
            "presentation.pptx", "text.txt", "spreadsheet.xlsx"
        ]
        for file in supported_files:
            assert worker.validFile(file) is True, f"{file} should be valid"

    def test_invalid_file_extensions(self):
        """Test invalid file extensions are rejected."""
        worker = DownloadWorker(queue.Queue(), None)
        
        # Test unsupported extensions
        unsupported_files = [
            "script.exe", "archive.rar", "video.mp4", 
            "random.xyz", "data.dat"
        ]
        for file in unsupported_files:
            assert worker.validFile(file) is False, f"{file} should be invalid"

    def test_download_file_success(self, mock_queue, mock_credentials):
        """Test successful file download scenario."""
        # Prepare test data
        test_file_id = "test_file_id"
        test_file_name = "test_document.pdf"
        
        # Create mock objects for services and download components
        mock_http = Mock()
        mock_service = Mock()
        mock_request = Mock()
        mock_downloader = Mock()
        
        # Configure mock objects
        mock_credentials.authorize = Mock(return_value=mock_http)
        
        # Patch discovery and file operations
        with patch('WorkerThreads.DownloadWorker.discovery.build', return_value=mock_service) as mock_build:
            with patch('WorkerThreads.DownloadWorker.open', mock_open()) as mock_file:
                with patch('os.path.exists', return_value=False):
                    # Create worker instance
                    worker = DownloadWorker(mock_queue, mock_credentials)
                    
                    # Configure mock service to return specific objects
                    mock_service.files().get_media.return_value = mock_request
                    
                    # Simulate download progress
                    mock_status = Mock()
                    mock_status.progress.return_value = 0.5
                    mock_downloader = Mock()
                    mock_downloader.next_chunk.return_value = (mock_status, False)
                    
                    # Patch MediaIoBaseDownload
                    with patch('WorkerThreads.DownloadWorker.MediaIoBaseDownload', return_value=mock_downloader):
                        # Call download method
                        worker.download_file(test_file_id, test_file_name)

                        # Verify interactions
                        mock_credentials.authorize.assert_called_once()
                        mock_build.assert_called_once_with("drive", "v3", http=mock_http)
                        mock_service.files().get_media.assert_called_once_with(fileId=test_file_id)
                        mock_file.assert_called_once()
                        mock_downloader.next_chunk.assert_called()