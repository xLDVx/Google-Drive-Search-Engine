import pytest
from datetime import datetime, timedelta
from tests.mock_google_drive_service import MockGoogleDriveService

def test_mock_drive_service_initialization():
    """Test initialization of mock Google Drive service."""
    service = MockGoogleDriveService()
    assert len(service.list_files()) == 2

def test_mock_drive_service_custom_initialization():
    """Test initialization with custom mock files."""
    custom_files = [
        {
            'id': 'custom1',
            'name': 'custom_doc.txt',
            'mimeType': 'text/plain',
            'content': 'Custom document content',
        }
    ]
    service = MockGoogleDriveService(mock_files=custom_files)
    assert len(service.list_files()) == 1
    assert service.list_files()[0]['name'] == 'custom_doc.txt'

def test_list_files_with_query():
    """Test filtering files with a query."""
    service = MockGoogleDriveService()
    
    # Filter by partial name match
    filtered_files = service.list_files(query='document1')
    assert len(filtered_files) == 1
    assert filtered_files[0]['name'] == 'document1.txt'

def test_get_file_metadata():
    """Test retrieving file metadata."""
    service = MockGoogleDriveService()
    
    # Get existing file metadata
    metadata = service.get_file_metadata('file1')
    assert metadata['name'] == 'document1.txt'
    assert 'createdTime' in metadata

def test_download_file():
    """Test downloading file content."""
    service = MockGoogleDriveService()
    
    # Download existing file
    content = service.download_file('file1')
    assert content == b'This is the content of document1.'

def test_file_not_found_errors():
    """Test error handling for non-existent files."""
    service = MockGoogleDriveService()
    
    # Metadata retrieval error
    with pytest.raises(FileNotFoundError):
        service.get_file_metadata('non_existent_file')
    
    # File download error
    with pytest.raises(FileNotFoundError):
        service.download_file('non_existent_file')

def test_add_file():
    """Test adding a new file to the mock service."""
    service = MockGoogleDriveService()
    
    # Add a new file
    new_file_data = {
        'name': 'new_document.txt',
        'mimeType': 'text/plain',
        'content': 'This is a new document.'
    }
    new_file_id = service.add_file(new_file_data)
    
    # Verify file was added
    assert len(service.list_files()) == 3
    added_file = service.get_file_metadata(new_file_id)
    assert added_file['name'] == 'new_document.txt'
    assert 'createdTime' in added_file

def test_add_file_missing_fields():
    """Test adding a file with missing required fields."""
    service = MockGoogleDriveService()
    
    # Attempt to add file without required fields
    with pytest.raises(ValueError):
        service.add_file({'content': 'Incomplete file data'})

def test_file_creation_time():
    """Test that file creation times are correctly set."""
    service = MockGoogleDriveService()
    
    # Add a new file and check its creation time
    new_file_data = {
        'name': 'timestamp_test.txt',
        'mimeType': 'text/plain',
        'content': 'Timestamp verification'
    }
    new_file_id = service.add_file(new_file_data)
    
    # Verify creation time is recent
    added_file = service.get_file_metadata(new_file_id)
    created_time = datetime.fromisoformat(added_file['createdTime'])
    assert datetime.now() - created_time < timedelta(seconds=1)