import pytest
from tests.mock_google_drive import MockGoogleDriveService
from datetime import datetime, timedelta

def test_mock_drive_service_initialization():
    """Test initialization of mock Google Drive service."""
    mock_service = MockGoogleDriveService()
    assert len(mock_service.execute()["files"]) == 2

def test_files_list_method():
    """Test files list method simulation."""
    mock_service = MockGoogleDriveService()
    files_response = mock_service.files().execute()
    assert "files" in files_response
    assert len(files_response["files"]) > 0

def test_get_file_metadata():
    """Test retrieving file metadata."""
    mock_service = MockGoogleDriveService()
    file_metadata = mock_service.get_file_metadata("file1")
    
    assert file_metadata["id"] == "file1"
    assert file_metadata["name"] == "document1.txt"
    assert file_metadata["mimeType"] == "text/plain"

def test_get_file_metadata_not_found():
    """Test error handling for non-existent file."""
    mock_service = MockGoogleDriveService()
    
    with pytest.raises(FileNotFoundError):
        mock_service.get_file_metadata("non_existent_file")

def test_download_file():
    """Test file download simulation."""
    mock_service = MockGoogleDriveService()
    
    # Test text file download
    text_file_content = mock_service.download_file("file1")
    assert text_file_content == b"Sample text document content"
    
    # Test spreadsheet file download
    spreadsheet_content = mock_service.download_file("file2")
    assert spreadsheet_content == b"Sample spreadsheet content"

def test_custom_mock_files():
    """Test initialization with custom mock files."""
    custom_files = [
        {
            "id": "custom1",
            "name": "custom_doc.pdf",
            "mimeType": "application/pdf",
            "createdTime": datetime.now().isoformat(),
            "size": "512",
            "owners": [{"displayName": "Custom User"}]
        }
    ]
    
    mock_service = MockGoogleDriveService(mock_files=custom_files)
    files_response = mock_service.files().execute()
    
    assert len(files_response["files"]) == 1
    assert files_response["files"][0]["name"] == "custom_doc.pdf"