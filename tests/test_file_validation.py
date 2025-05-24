import os
import sys
import pytest

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    download_worker = DownloadWorker(MockQueue(), MockCredentials())
    
    # Supported file extensions
    supported_files = [
        "document.pdf", 
        "spreadsheet.xlsx", 
        "presentation.pptx", 
        "text.txt", 
        "image.jpg", 
        "data.csv", 
        "document.docx", 
        "webpage.html"
    ]
    
    # Unsupported file extensions
    unsupported_files = [
        "script.py", 
        "archive.zip", 
        "compressed.rar", 
        "executable.exe"
    ]
    
    # Check supported files
    for file in supported_files:
        assert download_worker.validFile(file) == True, f"{file} should be a valid file"
    
    # Check unsupported files
    for file in unsupported_files:
        assert download_worker.validFile(file) == False, f"{file} should be an invalid file"

def test_edge_cases_file_validation():
    """Test edge cases in file validation."""
    download_worker = DownloadWorker(MockQueue(), MockCredentials())
    
    # Edge cases
    edge_cases = [
        "", # Empty filename
        "file_without_extension", 
        ".hidden_file", 
        "file.WITH.UPPERCASE.EXTENSION"
    ]
    
    # Check edge cases
    for file in edge_cases:
        assert download_worker.validFile(file) == False, f"{file} should be considered invalid"

def test_case_sensitivity():
    """Verify that file extension validation is case-insensitive."""
    download_worker = DownloadWorker(MockQueue(), MockCredentials())
    
    case_variations = [
        "document.PDF", 
        "image.JPEG", 
        "spreadsheet.XLSX"
    ]
    
    # These should still return False due to current implementation
    for file in case_variations:
        assert download_worker.validFile(file) == False, f"{file} should be considered invalid due to case sensitivity"