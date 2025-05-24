import os
import queue
import pytest
from unittest.mock import Mock, patch
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
        
        supported_files = [
            "document.pdf", "data.csv", "image.jpg", 
            "presentation.pptx", "text.txt", "spreadsheet.xlsx"
        ]
        unsupported_files = [
            "script.exe", "archive.rar", "video.mp4", 
            "random.xyz", "data.dat"
        ]

        # Verify supported extensions
        for file in supported_files:
            assert worker.validFile(file) is True, f"{file} should be valid"
        
        # Verify unsupported extensions
        for file in unsupported_files:
            assert worker.validFile(file) is False, f"{file} should be invalid"

    def test_download_worker_attributes(self, mock_queue, mock_credentials):
        """Test basic attributes of DownloadWorker."""
        worker = DownloadWorker(mock_queue, mock_credentials)
        
        assert worker.que == mock_queue
        assert worker.credentials == mock_credentials

    @patch('WorkerThreads.DownloadWorker.discovery')
    def test_download_file_method(self, mock_discovery, mock_credentials):
        """Validate download_file method basic interactions."""
        # Setup minimal mocks
        mock_service = Mock()
        mock_http = Mock()
        mock_request = Mock()
        mock_downloader = Mock()

        mock_credentials.authorize = Mock(return_value=mock_http)
        mock_discovery.build.return_value = mock_service
        mock_service.files().get_media.return_value = mock_request

        # Create a mock status object
        mock_status = Mock()
        mock_status.progress.return_value = 0.5
        mock_downloader.next_chunk.return_value = (mock_status, True)

        # Create worker
        worker = DownloadWorker(queue.Queue(), mock_credentials)

        # Patch file and download-related operations
        with patch('WorkerThreads.DownloadWorker.open', create=True):
            with patch('WorkerThreads.DownloadWorker.MediaIoBaseDownload', return_value=mock_downloader):
                with patch('os.path.join', return_value='/test/path/file.pdf'):
                    # Call method
                    worker.download_file("test_file_id", "test_file.pdf")

                    # Assert key interactions
                    mock_credentials.authorize.assert_called_once()
                    mock_discovery.build.assert_called_once()
                    mock_service.files().get_media.assert_called_once()