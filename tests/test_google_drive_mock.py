import pytest
from mock_services.google_drive_mock import MockGoogleDriveService

def test_mock_google_drive_service_initialization():
    """Test initialization of mock Google Drive service."""
    mock_service = MockGoogleDriveService()
    assert mock_service.mock_files is not None
    assert len(mock_service.mock_files) > 0

def test_list_files_without_query():
    """Test listing all files without a query."""
    mock_service = MockGoogleDriveService()
    files = mock_service.list_files()
    assert len(files) > 0
    assert all('id' in file and 'name' in file for file in files)

def test_list_files_with_query():
    """Test listing files with a specific query."""
    mock_files = [
        {'id': '1', 'name': 'report.pdf'},
        {'id': '2', 'name': 'presentation.pptx'},
        {'id': '3', 'name': 'notes.txt'}
    ]
    mock_service = MockGoogleDriveService(mock_files)
    
    pdf_files = mock_service.list_files('pdf')
    assert len(pdf_files) == 1
    assert pdf_files[0]['name'] == 'report.pdf'

def test_get_file_metadata():
    """Test retrieving file metadata."""
    mock_files = [
        {'id': 'file1', 'name': 'document.txt', 'size': 1024}
    ]
    mock_service = MockGoogleDriveService(mock_files)
    
    metadata = mock_service.get_file_metadata('file1')
    assert metadata is not None
    assert metadata['name'] == 'document.txt'
    assert metadata['size'] == 1024

def test_get_nonexistent_file_metadata():
    """Test retrieving metadata for a non-existent file."""
    mock_service = MockGoogleDriveService()
    metadata = mock_service.get_file_metadata('nonexistent_id')
    assert metadata is None

def test_download_file():
    """Test downloading a file."""
    mock_files = [
        {'id': 'file1', 'name': 'document.txt', 'content': 'Test content'}
    ]
    mock_service = MockGoogleDriveService(mock_files)
    
    file_content = mock_service.download_file('file1')
    assert file_content is not None
    assert file_content == b'Test content'

def test_download_nonexistent_file():
    """Test downloading a non-existent file."""
    mock_service = MockGoogleDriveService()
    file_content = mock_service.download_file('nonexistent_id')
    assert file_content is None

def test_export_file():
    """Test exporting a file."""
    mock_files = [
        {'id': 'file1', 'name': 'document.txt', 'content': 'Test export content'}
    ]
    mock_service = MockGoogleDriveService(mock_files)
    
    exported_content = mock_service.export_file('file1', 'text/plain')
    assert exported_content is not None
    assert exported_content == b'Test export content'

def test_export_nonexistent_file():
    """Test exporting a non-existent file."""
    mock_service = MockGoogleDriveService()
    exported_content = mock_service.export_file('nonexistent_id', 'text/plain')
    assert exported_content is None