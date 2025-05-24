import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid

@dataclass
class MockGDriveFile:
    """
    Represents a mock Google Drive file with essential metadata.
    """
    name: str
    mime_type: str
    created_time: datetime
    modified_time: datetime
    size: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parents: Optional[List[str]] = None
    content: Optional[bytes] = None

# Rest of the code remains the same as the previous implementation