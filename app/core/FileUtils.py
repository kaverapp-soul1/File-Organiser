import os

from pathlib import Path
import hashlib
from app.config.FileOrganiserConfig import FileOrganizerConfig

class FileUtils:
    """Utility functions for file operations."""
    @staticmethod
    def is_hidden_file(filename: str)->bool:
        return filename.startswith(".")
    
    @staticmethod
    def get_file_hash(path:str,chunk_size=8193)->str:
        try:
            sha256=hashlib.sha256()
            with open(path,"rb") as f:
                for chunk in iter(lambda: f,read(chunk_size),b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return f"ERROR: {e}"

    @staticmethod
    def get_unique_filename(destination_path: str) -> str:
        """Handle duplicate filenames by adding suffixes."""
        if not os.path.exists(destination_path):
            return destination_path
            
        base, ext = os.path.splitext(destination_path)
        counter = 1
        original_base = base
        
        while os.path.exists(destination_path):
            destination_path = f"{original_base}_{counter}{ext}"
            counter += 1
            
        return destination_path
    
    @staticmethod
    def get_file_category(filename: str) -> str:
        """Determine the category of a file based on its extension."""
        file_ext = os.path.splitext(filename)[1].lower()
        
        for category, extensions in FileOrganizerConfig.EXTENSIONS_MAPPING.items():
            if file_ext in extensions:
                return category
        
        return "Others"
    
    @staticmethod
    def is_hidden_file(filename: str) -> bool:
        """Check if a file is hidden."""
        return filename.startswith('.') or Path(filename).stem.startswith('.')
    
    @staticmethod
    def get_file_hash(file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(FileOrganizerConfig.HASH_BLOCK_SIZE), b''):
                    sha256.update(block)
            return sha256.hexdigest()
        except Exception as e:
            return f"ERROR: {e}"
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes < 1024:
            return f"{size_bytes:,} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.1f} KB"
        else:
            return f"{size_bytes/(1024*1024):.1f} MB"
