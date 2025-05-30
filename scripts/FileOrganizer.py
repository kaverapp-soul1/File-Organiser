import os
import shutil
import json

from typing import Dict, Tuple, Optional, Callable

from app.config.FileOrganiserConfig import FileOrganizerConfig
from app.core.FileLogger import FileLogger
from app.core.FileUtils import FileUtils

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileOrganizer:
    """Main file organizer class."""
    
    def __init__(self):
        self.logger = FileLogger()
        self.utils = FileUtils()
    
    def count_files_by_category(self, directory: str, include_hidden: bool = False) -> Dict[str, int]:
        """Count files in each category for preview."""
        category_counts = {category: 0 for category in FileOrganizerConfig.EXTENSIONS_MAPPING.keys()}
        
        try:
            for dirpath, _, filenames in os.walk(directory):
                for filename in filenames:
                    if not include_hidden and self.utils.is_hidden_file(filename):
                        continue
                    
                    category = self.utils.get_file_category(filename)
                    category_counts[category] += 1
        except Exception as e:
            logger.error(f"Error counting files: {e}")
        
        return category_counts
    
    def organize_files(self, root_directory: str, flatten_structure: bool = False, 
                      include_hidden: bool = False, progress_callback: Optional[Callable] = None) -> Tuple[bool, str]:
        """Organize files recursively with progress tracking."""
        if not os.path.exists(root_directory):
            return False, "Directory does not exist."
        
        # Count total files for progress tracking
        total_files = self._count_total_files(root_directory, include_hidden)
        
        if total_files == 0:
            return False, "No files found in the directory to organize."
        
        processed_files = 0
        errors = []
        
        # Organize files
        for dirpath, _, filenames in os.walk(root_directory):
            for filename in filenames:
                if not include_hidden and self.utils.is_hidden_file(filename):
                    continue
                
                result = self._move_file(dirpath, filename, root_directory, flatten_structure)
                if result['success']:
                    processed_files += 1
                else:
                    errors.append(result['error'])
                
                # Update progress
                if progress_callback:
                    progress_callback(processed_files / total_files)
        
        # Clean empty directories
        empty_dirs = self._clean_empty_directories(root_directory, flatten_structure)
        
        message = f"Processed {processed_files} files, cleaned {empty_dirs} empty directories."
        if errors:
            message += f" Encountered {len(errors)} errors."
        
        return True, message
    
    def _count_total_files(self, directory: str, include_hidden: bool) -> int:
        """Count total files in directory."""
        count = 0
        try:
            for dirpath, _, filenames in os.walk(directory):
                for filename in filenames:
                    if not include_hidden and self.utils.is_hidden_file(filename):
                        continue
                    count += 1
        except Exception as e:
            logger.error(f"Error counting total files: {e}")
        return count
    
    def _move_file(self, dirpath: str, filename: str, root_directory: str, flatten_structure: bool) -> Dict:
        """Move a single file to its category folder."""
        try:
            src_path = os.path.join(dirpath, filename)
            category = self.utils.get_file_category(filename)
            
            # Set destination path
            if flatten_structure:
                dest_dir = os.path.join(root_directory, category)
            else:
                dest_dir = os.path.join(dirpath, category)
            
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)
            
            # Handle duplicates
            dest_path = self.utils.get_unique_filename(dest_path)
            
            # Move file
            shutil.move(src_path, dest_path)
            self.logger.log_action("moves", src_path, dest_path)
            
            return {'success': True, 'error': None}
            
        except Exception as e:
            error_msg = f"Failed to move {filename}: {str(e)}"
            self.logger.log_action("errors", src_path, error_msg=error_msg)
            return {'success': False, 'error': error_msg}
    
    def _clean_empty_directories(self, root_directory: str, flatten_structure: bool) -> int:
        """Clean empty directories after organization."""
        empty_dirs = 0
        try:
            for dirpath, dirnames, filenames in list(os.walk(root_directory, topdown=False)):
                # Skip root directory and category directories if flattening
                if dirpath == root_directory:
                    continue
                
                if flatten_structure and os.path.basename(dirpath) in FileOrganizerConfig.EXTENSIONS_MAPPING.keys():
                    continue
                
                try:
                    if not os.listdir(dirpath):
                        os.rmdir(dirpath)
                        empty_dirs += 1
                except OSError as e:
                    error_msg = f"Failed to remove empty directory {dirpath}: {str(e)}"
                    self.logger.log_action("errors", dirpath, error_msg=error_msg)
        except Exception as e:
            logger.error(f"Error cleaning directories: {e}")
        
        return empty_dirs
    
    def undo_last_organization(self) -> Tuple[bool, str]:
        """Revert the last organization using the log file."""
        try:
            if not os.path.exists(self.logger.log_file):
                return False, "No log file found - nothing to undo."
            
            with open(self.logger.log_file, 'r') as f:
                data = json.load(f)
            
            if not data.get("moves"):
                return False, "No previous organization actions found to undo."
            
            undone_count = 0
            errors = []
            remaining_moves = []
            
            # Undo moves in reverse order
            for move in reversed(data["moves"]):
                try:
                    if os.path.exists(move["destination"]):
                        os.makedirs(os.path.dirname(move["source"]), exist_ok=True)
                        shutil.move(move["destination"], move["source"])
                        undone_count += 1
                    else:
                        errors.append(f"Destination file not found: {move['destination']}")
                        remaining_moves.append(move)
                except Exception as e:
                    errors.append(f"Failed to undo {move['destination']}: {str(e)}")
                    remaining_moves.append(move)
            
            # Update log file
            data["moves"] = remaining_moves
            with open(self.logger.log_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            message = f"Successfully undone {undone_count} file moves."
            if errors:
                message += f" {len(errors)} errors occurred."
            
            return True, message
            
        except Exception as e:
            logger.error(f"Error during undo: {e}")
            return False, f"Error during undo operation: {str(e)}"
    
    # def find_duplicates(self, directory: str, include_hidden: bool = False) -> Dict[str, List[str]]:
        """Find duplicate files based on SHA-256 hash."""
        hash_map = {}
        duplicates = {}
        
        try:
            for dirpath, _, filenames in os.scandir(directory):
                for filename in filenames:
                    if not include_hidden and self.utils.is_hidden_file(filename):
                        continue
                    
                    file_path = os.path.join(dirpath, filename)
                    
                    if os.path.isdir(file_path):
                        continue
                    
                    file_hash = self.utils.get_file_hash(file_path)
                    if file_hash.startswith("ERROR"):
                        self.logger.log_action("errors", file_path, error_msg=f"Hashing failed: {file_hash}")
                        continue
                    
                    if file_hash in hash_map:
                        if file_hash not in duplicates:
                            duplicates[file_hash] = [hash_map[file_hash]]
                        duplicates[file_hash].append(file_path)
                    else:
                        hash_map[file_hash] = file_path
                        
        except Exception as e:
            logger.error(f"Error finding duplicates: {e}")
        
        return duplicates
    
    def find_duplicates(self, directory: str, include_hidden: bool = False):
        from collections import defaultdict
        from concurrent.futures import ThreadPoolExecutor

        duplicates = defaultdict(list)
        hash_map = {}

        try:
            files = list(self._all_files(directory, include_hidden))

            def process_file(path):
                return (path, self.utils.get_file_hash(path))

            with ThreadPoolExecutor() as executor:
                for path, file_hash in executor.map(process_file, files):
                    if file_hash.startswith("ERROR"):
                        self.logger.log_action("errors", path, error_msg=f"Hashing failed: {file_hash}")
                        continue

                    if file_hash in hash_map:
                        duplicates[file_hash].append(path)
                        if len(duplicates[file_hash]) == 1:
                            duplicates[file_hash].append(hash_map[file_hash])
                    else:
                        hash_map[file_hash] = path

        except Exception as e:
            self.logger.log_action("errors", directory, error_msg=f"Error finding duplicates: {e}")

        return {k: list(set(v)) for k, v in duplicates.items()}
