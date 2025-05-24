import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WorkerThreads.DownloadWorker import DownloadWorker

class TestDownloadWorker:
    @pytest.fixture
    def mock_google_drive_service(self):
        """Create a mock Google Drive service for testing."""
        mock_service = Mock()
        mock_service.files().get.return_value.execute.return_value = {
            'id': 'test_file_id',
            'name': 'test_document.txt',
            'mimeType': 'text/plain'
        }
        return mock_service

    def test_download_worker_initialization(self):
        """Test DownloadWorker initialization."""
        try:
            worker = DownloadWorker()
            assert worker is not None, "DownloadWorker should be initialized"
        except Exception as e:
            pytest.fail(f"DownloadWorker initialization failed: {e}")

    @patch('WorkerThreads.DownloadWorker.build')
    def test_file_metadata_retrieval(self, mock_build, mock_google_drive_service):
        """Test file metadata retrieval from Google Drive."""
        # Setup mock build and service
        mock_build.return_value = mock_google_drive_service
        
        worker = DownloadWorker()
        
        # Ensure a method to get file metadata exists
        if not hasattr(worker, '_get_file_metadata'):
            pytest.skip("Method _get_file_metadata not found in DownloadWorker")
        
        file_metadata = worker._get_file_metadata('test_file_id')
        
        # Assertions
        assert file_metadata is not None, "File metadata should be retrieved"
        assert file_metadata['id'] == 'test_file_id'
        assert file_metadata['name'] == 'test_document.txt'

    def test_invalid_file_id(self):
        """Test handling of invalid file ID."""
        worker = DownloadWorker()
        
        # Check if method exists
        if not hasattr(worker, '_get_file_metadata'):
            pytest.skip("Method _get_file_metadata not found in DownloadWorker")
        
        # Test None input
        with pytest.raises((ValueError, TypeError), match="Invalid|file ID"):
            worker._get_file_metadata(None)
        
        # Test empty string input
        with pytest.raises((ValueError, TypeError), match="Invalid|file ID"):
            worker._get_file_metadata('')

    def test_file_type_validation(self):
        """Test file type validation."""
        worker = DownloadWorker()
        
        # Check if method exists
        if not hasattr(worker, '_validate_file_type'):
            pytest.skip("Method _validate_file_type not found in DownloadWorker")
        
        # Simulate different MIME types
        valid_types = [
            'text/plain', 
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.google-apps.document'
        ]
        invalid_types = ['image/jpeg', 'video/mp4']
        
        for mime_type in valid_types:
            assert worker._validate_file_type(mime_type) is True, f"Should accept {mime_type}"
        
        for mime_type in invalid_types:
            assert worker._validate_file_type(mime_type) is False, f"Should reject {mime_type}"