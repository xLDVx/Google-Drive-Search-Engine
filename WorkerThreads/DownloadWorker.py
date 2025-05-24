import threading
import queue
import os
import sys

class DownloadWorker(threading.Thread):
    def __init__(self, que, credentials, *args, **kwargs):
        self.que = que
        self.credentials = credentials
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            try:
                _file = self.que.get(timeout=3)
            except queue.Empty:
                return
            file_id = _file["id"]
            file_name = _file["name"]

            # To avoid downloading files that already exists
            if not os.path.exists(os.path.join("Data", "raw", file_name)) and self.validFile(_file["name"]):
                print(f"${file_name} downloading")
                self.download_file(file_id, file_name)

            # Task done for notifying que.join()
            self.que.task_done()

    def validFile(self, file_name):
        supportedExt = [".csv", ".doc", ".docx", ".epub", ".eml", ".gif", ".jpg", 
                        ".jpeg", ".json", ".html", ".htm", ".mp3", ".msg", ".odt", 
                        ".ogg", ".pdf", ".png", ".pptx", ".ps", ".rtf", ".tiff", 
                        ".tif", ".txt", ".wav", ".xlsx", ".xls"]
        pre, ext = os.path.splitext(os.path.basename(file_name))
        return ext.lower() in supportedExt

    def download_file(self, file_id, output_file):
        # Mock implementation
        pass