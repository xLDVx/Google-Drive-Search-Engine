import os
import sys
import pytest
from unittest.mock import MagicMock

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock external dependencies
sys.modules['apiclient'] = MagicMock()
sys.modules['apiclient.http'] = MagicMock()
sys.modules['apiclient.discovery'] = MagicMock()
sys.modules['oauth2client'] = MagicMock()
sys.modules['oauth2client.file'] = MagicMock()
sys.modules['httplib2'] = MagicMock()

from WorkerThreads.DownloadWorker import DownloadWorker

class MockQueue:
    def __init__(self):
        pass
    def get(self, timeout=None):
        return None
    def task_done(self):
        pass

def test_valid_file_extensions():
    """
    Test that various valid file extensions are correctly identified
    """
    download_worker = DownloadWorker(MockQueue(), None)
    
    # Test supported extensions
    supported_files = [
        "document.pdf", 
        "spreadsheet.xlsx", 
        "image.jpg", 
        "text.txt", 
        "presentation.pptx", 
        "document.docx"
    ]
    
    for file in supported_files:
        assert download_worker.validFile(file) is True, f"Failed to validate {file}"

def test_invalid_file_extensions():
    """
    Test that unsupported file extensions are rejected
    """
    download_worker = DownloadWorker(MockQueue(), None)
    
    # Test unsupported extensions
    unsupported_files = [
        "script.exe", 
        "archive.zip", 
        "file.rar", 
        "unknown.xyz"
    ]
    
    for file in unsupported_files:
        assert download_worker.validFile(file) is False, f"Incorrectly validated {file}"

def test_case_sensitivity():
    """
    Test that file extension validation is case-insensitive
    """
    download_worker = DownloadWorker(MockQueue(), None)
    
    # Test variations of case for supported extensions
    case_variations = [
        "document.PDF", 
        "image.JPG", 
        "spreadsheet.XLSX"
    ]
    
    for file in case_variations:
        assert download_worker.validFile(file) is False, f"Incorrectly validated case-sensitive {file}"

def test_empty_filename():
    """
    Test handling of empty or invalid filenames
    """
    download_worker = DownloadWorker(MockQueue(), None)
    
    invalid_filenames = [
        "", 
        None, 
        "   ", 
        "filename_without_extension"
    ]
    
    for filename in invalid_filenames:
        assert download_worker.validFile(filename) is False, f"Incorrectly validated empty/invalid filename {filename}"