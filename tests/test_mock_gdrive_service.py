import os
import pytest
from WorkerThreads.mock_gdrive_service import MockGDriveService

@pytest.fixture
def mock_gdrive_service():
    """Fixture to create a MockGDriveService for testing."""
    return MockGDriveService()

def test_list_files(mock_gdrive_service):
    """Test listing all files in the mock service."""
    files = mock_gdrive_service.list_files()
    assert len(files) == 3
    assert all('id' in file and 'name' in file and 'content' in file for file in files)

def test_list_files_with_query(mock_gdrive_service):
    """Test filtering files with a query."""
    ml_files = mock_gdrive_service.list_files('machine learning')
    assert len(ml_files) == 1
    assert ml_files[0]['name'] == 'document1.txt'

def test_get_file_content(mock_gdrive_service):
    """Test retrieving file content by ID."""
    content = mock_gdrive_service.get_file_content('file2')
    assert content == 'Artificial Intelligence is transforming various industries.'

def test_get_file_metadata(mock_gdrive_service):
    """Test retrieving file metadata by ID."""
    metadata = mock_gdrive_service.get_file_metadata('file3')
    assert metadata is not None
    assert 'content' not in metadata
    assert metadata['name'] == 'document3.docx'

def test_download_file(mock_gdrive_service, tmp_path):
    """Test downloading a mock file."""
    download_path = tmp_path / 'test_download.txt'
    result = mock_gdrive_service.download_file('file1', str(download_path))
    
    assert result is True
    assert os.path.exists(download_path)
    with open(download_path, 'r') as f:
        content = f.read()
    assert content == 'This is a sample text document about machine learning.'

def test_download_nonexistent_file(mock_gdrive_service, tmp_path):
    """Test downloading a nonexistent file."""
    download_path = tmp_path / 'nonexistent.txt'
    result = mock_gdrive_service.download_file('nonexistent_file', str(download_path))
    
    assert result is False
    assert not os.path.exists(download_path)