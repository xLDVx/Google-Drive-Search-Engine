import pytest
import os
from WorkerThreads.DownloadWorker import DownloadWorker
from tests.mock_gdrive_service import MockGDriveService

class TestDownloadWorker:
    @pytest.fixture
    def mock_files(self):
        """
        Fixture providing sample mock files for testing.
        """
        return [
            {
                'id': 'file1',
                'name': 'test_document.txt',
                'mimeType': 'text/plain',
                'content': b'Sample document content'
            },
            {
                'id': 'file2',
                'name': 'test_spreadsheet.xlsx',
                'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'content': b'Binary spreadsheet data'
            }
        ]

    @pytest.fixture
    def download_worker(self, mock_files):
        """
        Create a DownloadWorker with mock Google Drive service.
        """
        mock_service = MockGDriveService(mock_files)
        return DownloadWorker(mock_service)

    def test_list_files(self, download_worker, mock_files):
        """
        Test listing files from Google Drive.
        """
        files = download_worker.list_files()
        assert len(files) == len(mock_files)
        assert all(file['name'] in [f['name'] for f in mock_files] for file in files)

    def test_list_files_with_query(self, download_worker, mock_files):
        """
        Test listing files with a search query.
        """
        query_files = download_worker.list_files("document")
        assert len(query_files) == 1
        assert query_files[0]['name'] == 'test_document.txt'

    def test_download_file(self, download_worker, mock_files):
        """
        Test file download functionality.
        """
        file_id = 'file1'
        downloaded_file = download_worker.download_file(file_id)
        
        assert downloaded_file is not None
        assert downloaded_file == mock_files[0]['content']

    def test_download_nonexistent_file(self, download_worker):
        """
        Test handling of non-existent file download.
        """
        with pytest.raises(FileNotFoundError):
            download_worker.download_file('nonexistent_file')

    def test_file_metadata(self, download_worker, mock_files):
        """
        Test retrieving file metadata.
        """
        file_id = 'file2'
        metadata = download_worker.get_file_metadata(file_id)
        
        assert metadata['id'] == file_id
        assert metadata['name'] == 'test_spreadsheet.xlsx'
        assert metadata['mimeType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    def test_file_type_detection(self, download_worker, mock_files):
        """
        Test file type detection.
        """
        text_file = [f for f in mock_files if f['name'] == 'test_document.txt'][0]
        spreadsheet_file = [f for f in mock_files if f['name'] == 'test_spreadsheet.xlsx'][0]
        
        assert download_worker.detect_file_type(text_file) == 'text/plain'
        assert download_worker.detect_file_type(spreadsheet_file) == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'