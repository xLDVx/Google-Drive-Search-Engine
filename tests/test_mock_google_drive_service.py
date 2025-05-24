import os
import pytest
import tempfile
from tests.mocks.google_drive_service import MockGoogleDriveService

@pytest.fixture
def mock_drive_service():
    """
    Create a MockGoogleDriveService with a temporary directory for sample files.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        service = MockGoogleDriveService(mock_files_directory=temp_dir)
        
        # Prepare sample files for testing
        sample_files = [
            {'name': 'document1.txt', 'content': 'This is a test document.'},
            {'name': 'document2.pdf', 'content': 'Another test PDF document.'},
            {'name': 'spreadsheet.csv', 'content': 'Name,Age\nJohn,30\nJane,25'}
        ]
        service.create_sample_files(sample_files)
        
        yield service

def test_list_files(mock_drive_service):
    """
    Test listing files in the mock Google Drive service.
    """
    files = mock_drive_service.list_files()
    assert len(files) == 3
    assert all('id' in file and 'name' in file and 'mimeType' in file for file in files)

def test_list_files_with_query(mock_drive_service):
    """
    Test listing files with a query filter.
    """
    pdf_files = mock_drive_service.list_files(query='pdf')
    assert len(pdf_files) == 1
    assert pdf_files[0]['name'] == 'document2.pdf'

def test_download_file(mock_drive_service):
    """
    Test downloading a file from the mock service.
    """
    file_contents = mock_drive_service.download_file('document1.txt')
    assert file_contents.decode('utf-8') == 'This is a test document.'

def test_download_nonexistent_file(mock_drive_service):
    """
    Test downloading a non-existent file raises FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError):
        mock_drive_service.download_file('nonexistent.txt')

def test_file_metadata(mock_drive_service):
    """
    Test file metadata contains correct information.
    """
    files = mock_drive_service.list_files()
    file_names = [file['name'] for file in files]
    assert set(file_names) == {'document1.txt', 'document2.pdf', 'spreadsheet.csv'}
    
    # Check MIME types
    for file in files:
        assert file['mimeType'] is not None