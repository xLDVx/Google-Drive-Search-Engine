import os
import sys
import pytest
from unittest.mock import Mock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock external dependencies
import sys
sys.modules['apiclient'] = Mock()
sys.modules['httplib2'] = Mock()
sys.modules['oauth2client'] = Mock()

from WorkerThreads.DownloadWorker import DownloadWorker

class MockQueue:
    def __init__(self):
        pass
    def get(self, timeout=None):
        return None
    def task_done(self):
        pass

class MockCredentials:
    def __init__(self):
        pass

def test_valid_file_extensions():
    """Test that supported file extensions are correctly validated."""
    worker = DownloadWorker(MockQueue(), MockCredentials())
    
    # Test supported extensions
    supported_files = [
        "document.docx", "report.pdf", "data.csv", 
        "image.jpg", "presentation.pptx", "text.txt", 
        "spreadsheet.xlsx", "email.eml"
    ]
    
    for file_name in supported_files:
        assert worker.validFile(file_name) == True, f"{file_name} should be valid"

def test_invalid_file_extensions():
    """Test that unsupported file extensions are rejected."""
    worker = DownloadWorker(MockQueue(), MockCredentials())
    
    # Test unsupported extensions
    unsupported_files = [
        "script.exe", "archive.zip", "unknown.bin", 
        "malware.sh", "config.sys", "random.dat"
    ]
    
    for file_name in unsupported_files:
        assert worker.validFile(file_name) == False, f"{file_name} should be invalid"

def test_case_sensitivity():
    """Test that file validation is case-insensitive for extensions."""
    worker = DownloadWorker(MockQueue(), MockCredentials())
    
    case_variations = [
        "document.DOCX", "report.PDF", "image.JPEG", 
        "data.CSV", "presentation.PPTX"
    ]
    
    for file_name in case_variations:
        assert worker.validFile(file_name) == True, f"{file_name} should be valid"

def test_filename_with_special_characters():
    """Test file validation with special characters in filenames."""
    worker = DownloadWorker(MockQueue(), MockCredentials())
    
    special_files = [
        "report with spaces.pdf", 
        "file_with_underscores.txt", 
        "file-with-hyphens.docx", 
        "résumé.doc"
    ]
    
    for file_name in special_files:
        assert worker.validFile(file_name) == True, f"{file_name} should be valid"

def test_empty_filename():
    """Test handling of empty or None filename."""
    worker = DownloadWorker(MockQueue(), MockCredentials())
    
    assert worker.validFile("") == False
    
def test_filename_without_extension():
    """Test handling of files without an extension."""
    worker = DownloadWorker(MockQueue(), MockCredentials())
    
    assert worker.validFile("filename") == False
    assert worker.validFile("filename.") == False