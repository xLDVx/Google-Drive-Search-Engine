from typing import Dict, Any, List

class MockGDriveService:
    """
    Mock Google Drive service for unit testing file fetching logic.
    Simulates API interactions without making actual network calls.
    """
    def __init__(self, mock_files: List[Dict[str, Any]] = None):
        """
        Initialize mock service with predefined files.
        
        :param mock_files: List of mock file dictionaries
        """
        self.files = mock_files or []
    
    def list_files(self, query: str = None) -> List[Dict[str, Any]]:
        """
        Simulate listing files from Google Drive.
        
        :param query: Optional search query
        :return: List of matching files
        """
        if query:
            return [f for f in self.files if query.lower() in f.get('name', '').lower()]
        return self.files
    
    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Retrieve file metadata for a specific file.
        
        :param file_id: Unique identifier of the file
        :return: File metadata dictionary
        :raises FileNotFoundError: If file is not found
        """
        for file in self.files:
            if file.get('id') == file_id:
                return file
        raise FileNotFoundError(f"File with ID {file_id} not found")
    
    def download_file(self, file_id: str) -> bytes:
        """
        Simulate file download.
        
        :param file_id: Unique identifier of the file
        :return: File content as bytes
        :raises FileNotFoundError: If file is not found
        """
        for file in self.files:
            if file.get('id') == file_id:
                return file.get('content', b'')
        raise FileNotFoundError(f"File with ID {file_id} not found")