import os
import pytest
import tempfile
from tests.mock_services.mock_google_drive import MockGoogleDriveService, MockGoogleDriveFile

@pytest.fixture
def mock_drive_service():
    """Create a fresh mock Google Drive service for each test."""
    mock_files = [
        MockGoogleDriveFile(
            id='file1', 
            name='document1.txt', 
            mime_type='text/plain', 
            content=b'Hello, world!',
            size=13
        ),
        MockGoogleDriveFile(
            id='file2', 
            name='spreadsheet1.csv', 
            mime_type='text/csv', 
            content=b'name,value\nJohn,100\nJane,200',
            size=28
        )
    ]
    return MockGoogleDriveService(mock_files)

def test_list_files(mock_drive_service):
    """Test listing files in mock service."""
    files = mock_drive_service.list_files()
    assert len(files) == 2
    assert {file.name for file in files} == {'document1.txt', 'spreadsheet1.csv'}

def test_list_files_with_query(mock_drive_service):
    """Test filtering files with a query."""
    filtered_files = mock_drive_service.list_files('txt')
    assert len(filtered_files) == 1
    assert filtered_files[0].name == 'document1.txt'

def test_get_file_metadata(mock_drive_service):
    """Test retrieving file metadata."""
    file_metadata = mock_drive_service.get_file_metadata('file1')
    assert file_metadata is not None
    assert file_metadata.name == 'document1.txt'
    assert file_metadata.mime_type == 'text/plain'

def test_download_file(mock_drive_service):
    """Test downloading file content."""
    file_content = mock_drive_service.download_file('file1')
    assert file_content == b'Hello, world!'

def test_create_file_from_local():
    """Test creating a mock file from a local file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write('Test local file content')
        temp_file.close()
        
        try:
            mock_service = MockGoogleDriveService()
            mock_file = mock_service.create_file_from_local(temp_file.name)
            
            assert mock_file.name == os.path.basename(temp_file.name)
            assert mock_file.content == b'Test local file content'
            assert mock_file.mime_type == 'text/plain'
        finally:
            os.unlink(temp_file.name)

def test_add_mock_file(mock_drive_service):
    """Test adding a new mock file to the service."""
    new_file = MockGoogleDriveFile(
        id='file3', 
        name='newdocument.txt', 
        mime_type='text/plain', 
        content=b'New file content'
    )
    
    initial_file_count = len(mock_drive_service.list_files())
    mock_drive_service.add_mock_file(new_file)
    
    updated_files = mock_drive_service.list_files()
    assert len(updated_files) == initial_file_count + 1
    assert 'newdocument.txt' in {file.name for file in updated_files}