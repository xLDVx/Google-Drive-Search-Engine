import pytest
from tests.mocks.google_drive_service import MockGoogleDriveService

def test_list_files_default():
    """Test listing files without a query."""
    drive_service = MockGoogleDriveService()
    files = drive_service.list_files()
    
    assert len(files) == 2
    assert all('id' in file and 'name' in file for file in files)

def test_list_files_with_query():
    """Test filtering files with a query."""
    drive_service = MockGoogleDriveService()
    filtered_files = drive_service.list_files(query='document1')
    
    assert len(filtered_files) == 1
    assert filtered_files[0]['name'] == 'document1.txt'

def test_get_file_metadata():
    """Test retrieving file metadata by ID."""
    drive_service = MockGoogleDriveService()
    file_metadata = drive_service.get_file_metadata('file1')
    
    assert file_metadata is not None
    assert file_metadata['name'] == 'document1.txt'
    assert file_metadata['id'] == 'file1'

def test_get_file_metadata_not_found():
    """Test retrieving metadata for a non-existent file."""
    drive_service = MockGoogleDriveService()
    file_metadata = drive_service.get_file_metadata('non_existent_file')
    
    assert file_metadata is None

def test_download_file():
    """Test downloading file content."""
    drive_service = MockGoogleDriveService()
    file_content = drive_service.download_file('file1')
    
    assert file_content is not None
    assert file_content == b'This is a sample text document for testing.'

def test_download_file_not_found():
    """Test downloading a non-existent file."""
    drive_service = MockGoogleDriveService()
    file_content = drive_service.download_file('non_existent_file')
    
    assert file_content is None

def test_supported_file_types():
    """Test file type support detection."""
    drive_service = MockGoogleDriveService()
    
    assert drive_service.is_supported_file_type('text/plain') == True
    assert drive_service.is_supported_file_type('application/pdf') == True
    assert drive_service.is_supported_file_type('text/csv') == False

def test_custom_mock_files():
    """Test creating service with custom mock files."""
    custom_files = [
        {
            'id': 'custom1',
            'name': 'custom_document.txt',
            'mimeType': 'text/plain',
            'content': 'Custom file content',
            'webContentLink': 'https://example.com/custom.txt'
        }
    ]
    drive_service = MockGoogleDriveService(custom_files)
    
    assert len(drive_service.list_files()) == 1
    assert drive_service.list_files()[0]['name'] == 'custom_document.txt'