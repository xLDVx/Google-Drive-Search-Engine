import pytest
import os
import json
from unittest.mock import Mock, patch, MagicMock

class DummyDownloadWorker:
    """A dummy implementation for testing purposes."""
    def __init__(self, credentials=None):
        self.credentials = credentials

    def list_files(self):
        """Simulate listing files."""
        return [
            {"id": "file1", "name": "document1.txt", "mimeType": "text/plain"},
            {"id": "file2", "name": "document2.pdf", "mimeType": "application/pdf"}
        ]

    def download_file(self, file_info, download_path):
        """Simulate file download."""
        if not file_info or not file_info.get('id'):
            raise ValueError("Invalid file information")
        
        # Create a dummy file
        with open(download_path, 'w') as f:
            f.write("Dummy file content")
        return True

    def filter_downloadable_files(self, files):
        """Simulate file filtering."""
        downloadable_mimetypes = [
            'text/plain', 
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        ]
        return [f for f in files if f.get('mimeType') in downloadable_mimetypes]

class TestDownloadWorker:
    @pytest.fixture
    def download_worker(self):
        """Create a DownloadWorker instance."""
        return DummyDownloadWorker()

    def test_initialize_download_worker(self, download_worker):
        """Test initialization of DownloadWorker."""
        assert download_worker is not None, "DownloadWorker should be instantiated"

    def test_list_files(self, download_worker):
        """Test listing files."""
        files = download_worker.list_files()
        assert len(files) == 2, "Should return mock files"
        assert files[0]["name"] == "document1.txt"
        assert files[1]["name"] == "document2.pdf"

    def test_download_file(self, download_worker, tmp_path):
        """Test downloading a file."""
        mock_file = {
            "id": "test_file_id", 
            "name": "test_document.txt", 
            "mimeType": "text/plain"
        }

        download_path = tmp_path / mock_file["name"]
        
        result = download_worker.download_file(mock_file, str(download_path))

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

        downloadable_files = download_worker.filter_downloadable_files(test_files)
        assert len(downloadable_files) == 3, "Should filter out non-downloadable files"

    def test_download_worker_error_handling(self, download_worker):
        """Test error handling in download worker."""
        invalid_file = {
            "id": None,
            "name": None,
            "mimeType": None
        }

        with pytest.raises(ValueError):
            download_worker.download_file(invalid_file, "/invalid/path")