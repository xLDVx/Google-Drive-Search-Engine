import pytest
import os
import json
from unittest.mock import Mock, patch, MagicMock
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Import the DownloadWorker (adjust import as needed)
try:
    from WorkerThreads.DownloadWorker import DownloadWorker
except ImportError:
    print("Unable to import DownloadWorker. Please check the import path.")
    DownloadWorker = None

@pytest.mark.skipif(DownloadWorker is None, reason="DownloadWorker could not be imported")
class TestDownloadWorker:
    @pytest.fixture
    def mock_credentials(self):
        """Create a mock credentials object."""
        return Mock(spec=Credentials)

    @pytest.fixture
    def download_worker(self, mock_credentials):
        """Create a DownloadWorker instance with mock credentials."""
        return DownloadWorker(credentials=mock_credentials)

    def test_initialize_download_worker(self, download_worker):
        """Test initialization of DownloadWorker."""
        assert download_worker is not None, "DownloadWorker should be instantiated"

    @patch('googleapiclient.discovery.build')
    def test_list_files(self, mock_build, download_worker, mock_credentials):
        """Test listing files from Google Drive."""
        # Prepare mock files
        mock_files = [
            {"id": "file1", "name": "document1.txt", "mimeType": "text/plain"},
            {"id": "file2", "name": "document2.pdf", "mimeType": "application/pdf"}
        ]
        
        # Create mock service and response
        mock_service = MagicMock()
        mock_files_method = MagicMock()
        mock_files_method.list.return_value.execute.return_value = {"files": mock_files}
        mock_service.files.return_value = mock_files_method
        mock_build.return_value = mock_service

        # Call list files method
        files = download_worker.list_files()

        # Verify results
        assert len(files) == 2, "Should return all mock files"
        assert files[0]["name"] == "document1.txt"
        assert files[1]["name"] == "document2.pdf"

    @patch('googleapiclient.discovery.build')
    def test_download_file(self, mock_build, download_worker, mock_credentials, tmp_path):
        """Test downloading a file from Google Drive."""
        # Prepare mock file details
        mock_file = {
            "id": "test_file_id", 
            "name": "test_document.txt", 
            "mimeType": "text/plain"
        }

        # Create a temp file to simulate download
        download_path = tmp_path / mock_file["name"]
        
        # Mock service components
        mock_service = MagicMock()
        mock_media_download = MagicMock()
        mock_media_download.download.return_value = (Mock(), True)
        mock_service.files().get_media.return_value = mock_media_download
        mock_build.return_value = mock_service

        # Perform file download
        result = download_worker.download_file(mock_file, str(download_path))

        # Verify download
        assert result is True, "File download should be successful"
        assert os.path.exists(download_path), "Downloaded file should exist"

    def test_filter_downloadable_files(self, download_worker):
        """Test filtering downloadable files."""
        test_files = [
            {"name": "document.txt", "mimeType": "text/plain"},
            {"name": "image.jpg", "mimeType": "image/jpeg"},
            {"name": "spreadsheet.xlsx", "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
            {"name": "presentation.pptx", "mimeType": "application/vnd.openxmlformats-officedocument.presentationml.presentation"}
        ]

        # Filter files
        downloadable_files = download_worker.filter_downloadable_files(test_files)

        # Verify filtering
        assert len(downloadable_files) == 4, "All files should be downloadable"

    def test_download_worker_error_handling(self, download_worker, mock_credentials):
        """Test error handling in download worker."""
        # Prepare a mock file with invalid details
        invalid_file = {
            "id": None,  # Invalid file ID
            "name": None,
            "mimeType": None
        }

        # Test error scenarios
        with pytest.raises(ValueError):
            download_worker.download_file(invalid_file, "/invalid/path")