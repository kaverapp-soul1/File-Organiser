from config.FileOrganiserConfig import FileOrganizerConfig
import json
import os
from datetime import datetime
from typing import Optional

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileLogger:
    """Handles logging of file operations."""
    
    def __init__(self, log_file: str = FileOrganizerConfig.LOG_FILE):
        self.log_file = log_file
        self.setup_logging()
    
    def setup_logging(self) -> None:
        """Initialize or load the log file."""
        try:
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w') as f:
                    json.dump({"moves": [], "errors": []}, f)
        except Exception as e:
            logger.error(f"Failed to setup logging: {e}")
    
    def log_action(self, action_type: str, source: str, destination: Optional[str] = None, error_msg: Optional[str] = None) -> None:
        """Log file movements and errors."""
        try:
            # Read existing data
            data = {"moves": [], "errors": []}
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
            
            # Add new entry
            entry = {
                "timestamp": datetime.now().strftime(FileOrganizerConfig.DATE_FORMAT),
                "source": source,
                "destination": destination,
                "error": error_msg
            }
            
            if action_type not in data:
                data[action_type] = []
            
            data[action_type].append(entry)
            
            # Write updated data
            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            logger.error(f"Failed to log action: {e}")
