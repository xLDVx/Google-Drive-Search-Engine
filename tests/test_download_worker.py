import pytest
import os
import json
from unittest.mock import Mock, patch
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Import the DownloadWorker (adjust import as needed)
from WorkerThreads.DownloadWorker import DownloadWorker

class MockGoogleDriveService:
    """Mock Google Drive service for testing."""
    def __init__(self, files=None):
        self.files = files or []

    def list(self, **kwargs):
        return Mock(execute=lambda: {"files": self.files})

    def get_media(self, fileId):
        return Mock()

class TestDownloadWorker:
    @pytest.fixture
    def mock_credentials(self):
        """Create a mock credentials object."""
        return Mock(spec=Credentials)

    @pytest.fixture
    def download_worker(self, mock_credentials):
        """Create a DownloadWorker instance with mock credentials."""
        return DownloadWorker(mock_credentials)

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
        
        # Create mock service with predefined files
        mock_service = MockGoogleDriveService(files=mock_files)
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
        
        # Mock download method
        mock_service = Mock()
        mock_media_download = Mock()
        mock_media_download.download.return_value = (Mock(), True)
        mock_service.files().get_media.return_value = mock_media_download
        mock_build.return_value = mock_service

        # Perform file download
        result = download_worker.download_file(mock_file, str(download_path))

        # Verify download
        assert result is True, "File download should be successful"
        assert download_path.exists(), "Downloaded file should exist"

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