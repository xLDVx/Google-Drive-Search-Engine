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

    @patch('os.path.exists')
    @patch('WorkerThreads.DownloadWorker.discovery')
    def test_download_file_success(self, mock_discovery, mock_exists, mock_queue, mock_credentials):
        """Test successful file download scenario."""
        # Simulate file does not exist
        mock_exists.return_value = False

        # Mock discovery service and download components
        mock_service = Mock()
        mock_request = Mock()
        mock_downloader = Mock()

        mock_discovery.build.return_value = mock_service
        mock_service.files().get_media.return_value = mock_request
        
        # Simulate download progress
        mock_downloader.next_chunk.return_value = (Mock(progress=lambda: 0.5), False)

        # Create worker and test file download
        worker = DownloadWorker(mock_queue, mock_credentials)
        
        with patch('builtins.open', create=True) as mock_file:
            with patch('WorkerThreads.DownloadWorker.MediaIoBaseDownload', return_value=mock_downloader):
                worker.download_file("test_file_id", "test_file.pdf")

                # Verify interactions
                mock_service.files().get_media.assert_called_once_with(fileId="test_file_id")
                mock_file.assert_called_once()
                mock_downloader.next_chunk.assert_called()

    def test_worker_queue_processing(self, mock_queue, mock_credentials):
        """Test worker processes queue items correctly."""
        # Prepare test files
        test_files = [
            {"id": "file1", "name": "document1.pdf"},
            {"id": "file2", "name": "image.jpg"}
        ]

        # Put files in queue
        for file in test_files:
            mock_queue.put(file)

        # Create worker and patch download method
        with patch.object(DownloadWorker, 'download_file') as mock_download:
            with patch.object(DownloadWorker, 'validFile', return_value=True):
                worker = DownloadWorker(mock_queue, mock_credentials)
                worker.run()

                # Verify download method called for each file
                assert mock_download.call_count == len(test_files)