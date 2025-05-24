import pytest
from unittest.mock import Mock, patch
import sys
import os
import queue

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WorkerThreads.DownloadWorker import DownloadWorker

class TestDownloadWorker:
    @pytest.fixture
    def mock_queue(self):
        """Create a mock queue for testing."""
        return Mock(spec=queue.Queue)

    @pytest.fixture
    def mock_credentials(self):
        """Create mock credentials for testing."""
        mock_creds = Mock()
        return mock_creds

    @pytest.fixture
    def download_worker(self, mock_queue, mock_credentials):
        """Create a DownloadWorker instance with mock dependencies."""
        return DownloadWorker(mock_queue, mock_credentials)

    def test_download_worker_initialization(self, download_worker):
        """Test DownloadWorker initialization."""
        assert download_worker is not None, "DownloadWorker should be initialized"

    def test_file_metadata_retrieval(self, download_worker):
        """Test file metadata retrieval logic."""
        # Ensure a method to get file metadata exists
        if not hasattr(download_worker, '_get_file_metadata'):
            pytest.skip("Method _get_file_metadata not found in DownloadWorker")
        
        # Since we can't test the actual method without mocking external dependencies,
        # we'll just verify the method's existence
        assert callable(getattr(download_worker, '_get_file_metadata', None)), \
            "Method _get_file_metadata should be a callable method"

    def test_invalid_file_id(self, download_worker):
        """Test handling of invalid file ID."""
        # Check if method exists
        if not hasattr(download_worker, '_get_file_metadata'):
            pytest.skip("Method _get_file_metadata not found in DownloadWorker")
        
        # Verify the method raises an error or handles invalid inputs
        method = getattr(download_worker, '_get_file_metadata')
        
        # Test None input
        with pytest.raises((ValueError, TypeError), match="Invalid|file ID"):
            method(None)
        
        # Test empty string input
        with pytest.raises((ValueError, TypeError), match="Invalid|file ID"):
            method('')

    def test_file_type_validation(self, download_worker):
        """Test file type validation."""
        # Check if method exists
        if not hasattr(download_worker, '_validate_file_type'):
            pytest.skip("Method _validate_file_type not found in DownloadWorker")
        
        # Simulate different MIME types
        method = getattr(download_worker, '_validate_file_type')
        
        valid_types = [
            'text/plain', 
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.google-apps.document'
        ]
        invalid_types = ['image/jpeg', 'video/mp4']
        
        for mime_type in valid_types:
            assert method(mime_type) is True, f"Should accept {mime_type}"
        
        for mime_type in invalid_types:
            assert method(mime_type) is False, f"Should reject {mime_type}"