import os
import sys
import pytest

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    
    # Valid file extensions from the original implementation
    valid_extensions = [
        ".csv", ".doc", ".docx", ".epub", ".eml", ".gif", ".jpg", 
        ".jpeg", ".json", ".html", ".htm", ".mp3", ".msg", ".odt", 
        ".ogg", ".pdf", ".png", ".pptx", ".ps", ".rtf", ".tiff", 
        ".tif", ".txt", ".wav", ".xlsx", ".xls"
    ]
    
    for ext in valid_extensions:
        test_filename = f"sample_document{ext}"
        assert download_worker.validFile(test_filename) == True, f"Failed to validate {ext} extension"

def test_invalid_file_extensions():
    """Test that unsupported file extensions are rejected."""
    download_worker = DownloadWorker(MockQueue(), MockCredentials())
    
    invalid_extensions = [
        ".zip", ".rar", ".exe", ".bin", ".sh", 
        ".py", ".jar", ".dmg", ".iso"
    ]
    
    for ext in invalid_extensions:
        test_filename = f"sample_document{ext}"
        assert download_worker.validFile(test_filename) == False, f"Incorrectly validated {ext} extension"

def test_case_sensitivity():
    """Verify that file extension validation is case-insensitive."""
    download_worker = DownloadWorker(MockQueue(), MockCredentials())
    
    test_cases = [
        "document.PDF", "DOCUMENT.DOCX", "file.TXT", 
        "image.JPG", "spreadsheet.XLSX"
    ]
    
    for filename in test_cases:
        # Extract the lowercase extension for validation
        assert download_worker.validFile(filename) == True, f"Failed to validate case-sensitive extension: {filename}"

def test_filename_variations():
    """Test file validation with complex filenames."""
    download_worker = DownloadWorker(MockQueue(), MockCredentials())
    
    test_cases = [
        "My Document.docx",
        "Report 2023.pdf",
        "Image_with_underscores.jpg",
        "file with spaces.txt",
        "complex.file.name.xlsx"
    ]
    
    for filename in test_cases:
        ext = os.path.splitext(filename)[1]
        expected_result = ext in [".docx", ".pdf", ".jpg", ".txt", ".xlsx"]
        assert download_worker.validFile(filename) == expected_result, f"Incorrect validation for filename: {filename}"

def test_empty_filename():
    """Test validation with an empty filename."""
    download_worker = DownloadWorker(MockQueue(), MockCredentials())
    
    assert download_worker.validFile("") == False, "Empty filename should not be valid"

def test_filename_without_extension():
    """Test validation for files without an extension."""
    download_worker = DownloadWorker(MockQueue(), MockCredentials())
    
    assert download_worker.validFile("filename") == False, "Filename without extension should not be valid"