import pytest
from datetime import datetime, timedelta
from tests.mock_google_drive_service import MockGoogleDriveService

@pytest.fixture
def mock_drive_service():
    """
    Fixture to create a MockGoogleDriveService for testing.
    """
    return MockGoogleDriveService()

def test_list_files(mock_drive_service):
    """
    Test listing files in the mock Google Drive service.
    """
    files = mock_drive_service.list_files()
    assert len(files) == 3
    assert all('id' in file and 'name' in file for file in files)

def test_list_files_with_page_size(mock_drive_service):
    """
    Test listing files with a specific page size.
    """
    files = mock_drive_service.list_files(page_size=2)
    assert len(files) == 2

def test_list_files_with_query(mock_drive_service):
    """
    Test filtering files with a query.
    """
    files = mock_drive_service.list_files(query='document')
    assert len(files) == 1
    assert files[0]['name'] == 'document1.txt'

def test_get_file_metadata(mock_drive_service):
    """
    Test retrieving file metadata by ID.
    """
    file_metadata = mock_drive_service.get_file_metadata('file1')
    assert file_metadata['name'] == 'document1.txt'
    assert file_metadata['mimeType'] == 'text/plain'

def test_get_file_metadata_not_found(mock_drive_service):
    """
    Test handling of non-existent file metadata.
    """
    with pytest.raises(FileNotFoundError):
        mock_drive_service.get_file_metadata('non_existent_file')

def test_download_file(mock_drive_service):
    """
    Test downloading file content.
    """
    file_content = mock_drive_service.download_file('file1')
    assert file_content == 'Sample text content for document1'

def test_download_file_not_found(mock_drive_service):
    """
    Test handling of file download for non-existent file.
    """
    with pytest.raises(FileNotFoundError):
        mock_drive_service.download_file('non_existent_file')

def test_mock_file_metadata_completeness(mock_drive_service):
    """
    Test that mock files have all required metadata.
    """
    required_keys = ['id', 'name', 'mimeType', 'size', 'createdTime', 'content']
    
    for file in mock_drive_service.list_files():
        assert all(key in file for key in required_keys)
        
        # Check type and basic validation of metadata
        assert isinstance(file['id'], str)
        assert isinstance(file['name'], str)
        assert isinstance(file['mimeType'], str)
        assert isinstance(file['size'], int)
        
        # Validate timestamp
        try:
            datetime.fromisoformat(file['createdTime'])
        except ValueError:
            pytest.fail(f"Invalid timestamp format for file {file['id']}")