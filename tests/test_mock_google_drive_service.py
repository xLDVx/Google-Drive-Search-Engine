import pytest
from tests.mocks.google_drive_service import MockGoogleDriveService
from datetime import datetime, timedelta

def test_mock_drive_service_initialization():
    """Test initializing MockGoogleDriveService with default files."""
    drive_service = MockGoogleDriveService()
    assert len(drive_service._files) == 2, "Default mock files should be 2"

def test_list_files_default():
    """Test listing files without any filters."""
    drive_service = MockGoogleDriveService()
    result = drive_service.list_files()
    assert 'files' in result
    assert len(result['files']) == 2
    assert result['nextPageToken'] is None

def test_list_files_with_query():
    """Test filtering files using a query."""
    drive_service = MockGoogleDriveService()
    result = drive_service.list_files(query='sample')
    assert len(result['files']) > 0
    assert all('sample' in file['name'] for file in result['files'])

def test_list_files_page_size():
    """Test page size limitation."""
    custom_files = [
        {'id': f'file{i}', 'name': f'document_{i}.txt'} 
        for i in range(10)
    ]
    drive_service = MockGoogleDriveService(mock_files=custom_files)
    result = drive_service.list_files(page_size=5)
    assert len(result['files']) == 5
    assert result['nextPageToken'] is not None

def test_get_file_metadata():
    """Test retrieving file metadata by ID."""
    drive_service = MockGoogleDriveService()
    metadata = drive_service.get_file_metadata('file1')
    assert metadata['id'] == 'file1'
    assert 'name' in metadata
    assert 'mimeType' in metadata

def test_get_file_metadata_not_found():
    """Test error handling for non-existent file."""
    drive_service = MockGoogleDriveService()
    with pytest.raises(ValueError, match="File with ID non_existent not found"):
        drive_service.get_file_metadata('non_existent')

def test_download_file():
    """Test downloading file content."""
    drive_service = MockGoogleDriveService()
    content = drive_service.download_file('file1')
    assert isinstance(content, bytes)
    assert b'sample text document' in content.lower()

def test_download_file_not_found():
    """Test error handling for downloading non-existent file."""
    drive_service = MockGoogleDriveService()
    with pytest.raises(ValueError, match="File with ID non_existent not found"):
        drive_service.download_file('non_existent')

def test_add_mock_file():
    """Test adding a new mock file to the service."""
    drive_service = MockGoogleDriveService()
    initial_file_count = len(drive_service._files)
    
    new_file = {
        'name': 'new_test_file.pdf',
        'mimeType': 'application/pdf',
        'content': b'Mock PDF content'
    }
    
    file_id = drive_service.add_mock_file(new_file)
    
    assert len(drive_service._files) == initial_file_count + 1
    assert any(file['name'] == 'new_test_file.pdf' for file in drive_service._files)
    assert file_id is not None

def test_custom_mock_files():
    """Test creating mock service with custom files."""
    custom_files = [
        {
            'id': 'custom1',
            'name': 'custom_document.txt',
            'content': 'Custom file content'
        }
    ]
    drive_service = MockGoogleDriveService(mock_files=custom_files)
    
    assert len(drive_service._files) == 1
    assert drive_service._files[0]['name'] == 'custom_document.txt'