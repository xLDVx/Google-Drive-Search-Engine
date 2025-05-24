import pytest
from mock_services.google_drive_mock import MockGoogleDriveService

def test_mock_drive_service_initialization():
    """Test initialization of MockGoogleDriveService."""
    mock_service = MockGoogleDriveService()
    assert len(mock_service.files().execute()['files']) > 0

def test_custom_file_list():
    """Test creating mock service with custom file list."""
    custom_files = [
        {
            'id': 'custom1',
            'name': 'custom_document.txt',
            'mimeType': 'text/plain',
            'size': '512'
        }
    ]
    mock_service = MockGoogleDriveService(mock_files=custom_files)
    files = mock_service.files().execute()['files']
    assert len(files) == 1
    assert files[0]['name'] == 'custom_document.txt'

def test_files_get_method():
    """Test files_get method retrieval."""
    mock_service = MockGoogleDriveService()
    file1 = mock_service.files_get('file1').execute()
    assert file1['id'] == 'file1'
    assert file1['name'] == 'document1.txt'

def test_download_file():
    """Test file download simulation."""
    mock_service = MockGoogleDriveService()
    mock_service.set_file_content('file1', 'Test file content')
    downloaded_content = mock_service.download_file('file1')
    assert downloaded_content == b'Test file content'

def test_download_nonexistent_file():
    """Test downloading a file with no content raises an error."""
    mock_service = MockGoogleDriveService()
    with pytest.raises(FileNotFoundError):
        mock_service.download_file('nonexistent_file')

def test_files_get_nonexistent_file():
    """Test retrieving metadata for a nonexistent file."""
    mock_service = MockGoogleDriveService()
    with pytest.raises(FileNotFoundError):
        mock_service.files_get('nonexistent_file')