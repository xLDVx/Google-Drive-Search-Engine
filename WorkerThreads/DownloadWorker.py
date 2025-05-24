import threading
import queue
import os
from apiclient.http import MediaIoBaseDownload, MediaFileUpload
from apiclient import discovery
from oauth2client.file import Storage
import io
import httplib2
import logging

class DownloadWorker(threading.Thread):
    def __init__(self, que, credentials, *args, **kwargs):
        """
        Initialize DownloadWorker with queue and credentials.
        
        :param que: Queue for file download tasks
        :param credentials: Google Drive API credentials
        """
        self.que = que
        self.credentials = credentials
        super().__init__(*args, **kwargs)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Main thread run method to process download tasks from queue.
        Handles queue timeout and task processing.
        """
        while True:
            try:
                # Get file from queue with timeout
                _file = self.que.get(timeout=3)
                file_id = _file.get("id")
                file_name = _file.get("name")

                # Validate input
                if not file_id or not file_name:
                    self.logger.warning(f"Invalid file entry: {_file}")
                    self.que.task_done()
                    continue

                # Check file existence and validity before download
                download_path = os.path.join("Data", "raw", file_name)
                if not os.path.exists(download_path) and self.validFile(file_name):
                    try:
                        self.logger.info(f"Downloading {file_name}")
                        self.download_file(file_id, file_name)
                    except Exception as e:
                        self.logger.error(f"Download failed for {file_name}: {e}")
                        # Optionally, you could implement retry logic or log to a separate error queue

                # Mark task as done
                self.que.task_done()

            except queue.Empty:
                # No more tasks in queue, exit thread
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in download worker: {e}")
                break

    def validFile(self, file_name):
        """
        Validate file based on supported extensions.
        
        :param file_name: Name of the file to validate
        :return: Boolean indicating if file is supported
        """
        supportedExt = [
            ".csv", ".doc", ".docx", ".epub", ".eml", ".gif", 
            ".jpg", ".jpeg", ".json", ".html", ".htm", ".mp3", 
            ".msg", ".odt", ".ogg", ".pdf", ".png", ".pptx", 
            ".ps", ".rtf", ".tiff", ".tif", ".txt", ".wav", 
            ".xlsx", ".xls"
        ]
        _, ext = os.path.splitext(os.path.basename(file_name))
        return ext.lower() in supportedExt

    def download_file(self, file_id, output_file):
        """
        Download a file from Google Drive.
        
        :param file_id: Unique identifier of the file
        :param output_file: Name of the output file
        :raises ValueError: For invalid input
        :raises Exception: For download failures
        """
        # Input validation
        if file_id is None or not file_id:
            raise ValueError("Invalid file ID")
        if output_file is None or not output_file:
            raise ValueError("Invalid output file name")

        try:
            # Authorize and build service
            http = self.credentials.authorize(httplib2.Http())
            service = discovery.build("drive", "v3", http=http)
            
            # Request file media
            request = service.files().get_media(fileId=file_id)
            
            # Prepare download
            download_path = os.path.join("Data", "raw", output_file)
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            
            with open(download_path, "wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    self.logger.info(f"Download progress for {output_file}: {int(status.progress() * 100)}%")

            self.logger.info(f"Successfully downloaded {output_file}")
            return True

        except Exception as e:
            self.logger.error(f"Download failed for {output_file}: {e}")
            raise