import pytest
import os
import queue
import threading
from unittest.mock import MagicMock

# Import the actual DownloadWorker
from WorkerThreads.DownloadWorker import DownloadWorker

class TestDownloadWorker:
    @pytest.fixture
    def mock_credentials(self):
        """
        Create mock credentials for testing.
        """
        mock_creds = MagicMock()
        mock_creds.authorize.return_value = MagicMock()
        return mock_creds

    @pytest.fixture
    def mock_queue(self):
        """
        Create a mock queue for testing.
        """
        return queue.Queue()

    @pytest.fixture
    def sample_files(self):
        """
        Provide sample file data for testing.
        """
        return [
            {
                "id": "file1",
                "name": "document.txt",
                "mimeType": "text/plain"
            },
            {
                "id": "file2",
                "name": "spreadsheet.xlsx",
                "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
        ]

    def test_valid_file_extensions(self, mock_credentials, mock_queue):
        """
        Test the valid file extension detection.
        """
        download_worker = DownloadWorker(mock_queue, mock_credentials)
        
        valid_files = [
            "document.txt", "report.csv", "presentation.pptx", 
            "image.jpg", "data.pdf", "spreadsheet.xlsx"
        ]
        
        invalid_files = [
            "script.py", "config.yaml", "unknown.bin"
        ]
        
        for file in valid_files:
            assert download_worker.validFile(file) is True, f"{file} should be considered valid"
        
        for file in invalid_files:
            assert download_worker.validFile(file) is False, f"{file} should be considered invalid"

    def test_worker_initialization(self, mock_credentials, mock_queue):
        """
        Test Download Worker initialization.
        """
        download_worker = DownloadWorker(mock_queue, mock_credentials)
        
        assert isinstance(download_worker, threading.Thread)
        assert download_worker.que == mock_queue
        assert download_worker.credentials == mock_credentials

    def test_download_file_processing(self, mock_credentials, mock_queue, sample_files, tmp_path):
        """
        Test file download processing logic.
        Mock the download process to simulate file retrieval.
        """
        # Mock the Data/raw directory
        os.makedirs(os.path.join(tmp_path, "Data", "raw"), exist_ok=True)
        
        # Temporarily replace the download directory for testing
        original_dir = os.path.join("Data", "raw")
        os.environ['DOWNLOAD_DIR'] = str(tmp_path)

        try:
            # Set up the mock queue with test files
            for file in sample_files:
                mock_queue.put(file)

            # Mock the download_file method to simulate file download
            DownloadWorker.download_file = MagicMock()

            # Create and start the download worker
            download_worker = DownloadWorker(mock_queue, mock_credentials)
            download_worker.start()
            download_worker.join()  # Wait for thread to complete

            # Verify queue processing
            assert mock_queue.empty()

            # Verify download_file was called for valid files
            download_calls = DownloadWorker.download_file.call_count
            assert download_calls == len(sample_files)

        finally:
            # Restore original download directory
            del os.environ['DOWNLOAD_DIR']