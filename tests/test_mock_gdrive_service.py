import pytest
from datetime import datetime, timedelta
from mock_services.mock_gdrive_service import MockGDriveService, MockGDriveFile

@pytest.fixture
def mock_gdrive_service():
    """
    Fixture to create a MockGDriveService for testing.
    """
    base_time = datetime.now()
    mock_files = [
        MockGDriveFile(
            id='test_file1',
            name='test_document1.pdf',
            mime_type='application/pdf',
            created_time=base_time - timedelta(days=10),
            modified_time=base_time - timedelta(days=5),
            size=1024 * 100,
            content=b'Test PDF content'
        ),
        MockGDriveFile(
            id='test_file2',
            name='test_report.docx',
            mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            created_time=base_time - timedelta(days=15),
            modified_time=base_time - timedelta(days=2),
            size=1024 * 200,
            content=b'Test Word document content'
        )
    ]
    return MockGDriveService(mock_files)

def test_list_files(mock_gdrive_service):
    """
    Test file listing functionality.
    """
    files = mock_gdrive_service.list_files()
    assert len(files) == 2
    assert all(isinstance(file, MockGDriveFile) for file in files)

def test_list_files_with_query(mock_gdrive_service):
    """
    Test file listing with query filtering.
    """
    pdf_files = mock_gdrive_service.list_files(query='pdf')
    assert len(pdf_files) == 1
    assert pdf_files[0].name == 'test_document1.pdf'

def test_get_file_metadata(mock_gdrive_service):
    """
    Test retrieving file metadata.
    """
    file_metadata = mock_gdrive_service.get_file_metadata('test_file1')
    assert file_metadata is not None
    assert file_metadata.id == 'test_file1'
    assert file_metadata.mime_type == 'application/pdf'

def test_download_file(mock_gdrive_service):
    """
    Test file download functionality.
    """
    file_content = mock_gdrive_service.download_file('test_file2')
    assert file_content is not None
    assert b'Test Word document content' in file_content

def test_create_file(mock_gdrive_service):
    """
    Test creating a new file.
    """
    new_file = MockGDriveFile(
        name='new_test_file.txt',
        mime_type='text/plain',
        created_time=datetime.now(),
        modified_time=datetime.now(),
        size=100,
        content=b'New test file content'
    )
    new_file_id = mock_gdrive_service.create_file(new_file)
    assert new_file_id is not None
    
    retrieved_file = mock_gdrive_service.get_file_metadata(new_file_id)
    assert retrieved_file is not None
    assert retrieved_file.name == 'new_test_file.txt'

def test_delete_file(mock_gdrive_service):
    """
    Test file deletion functionality.
    """
    initial_file_count = len(mock_gdrive_service.list_files())
    deletion_result = mock_gdrive_service.delete_file('test_file1')
    
    assert deletion_result is True
    assert len(mock_gdrive_service.list_files()) == initial_file_count - 1
    assert mock_gdrive_service.get_file_metadata('test_file1') is None

def test_file_ordering(mock_gdrive_service):
    """
    Test file listing with different ordering.
    """
    created_time_ordered = mock_gdrive_service.list_files(order_by='createdTime')
    assert len(created_time_ordered) == 2
    assert created_time_ordered[0].name == 'test_report.docx'  # Older file first

def test_nonexistent_file_handling(mock_gdrive_service):
    """
    Test handling of nonexistent files.
    """
    nonexistent_metadata = mock_gdrive_service.get_file_metadata('nonexistent_id')
    assert nonexistent_metadata is None

    nonexistent_download = mock_gdrive_service.download_file('nonexistent_id')
    assert nonexistent_download is None

    deletion_result = mock_gdrive_service.delete_file('nonexistent_id')
    assert deletion_result is False