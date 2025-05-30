# import streamlit as st
# import os
# import shutil
# import json
# from datetime import datetime
# from pathlib import Path
# import time
# import hashlib
# from typing import Dict, List, Tuple, Optional, Callable
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class FileOrganizerConfig:
#     """Configuration constants for the file organizer."""
#     LOG_FILE = "file_organizer_log.json"
#     DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"
#     HASH_BLOCK_SIZE = 65536
    
#     EXTENSIONS_MAPPING = {
#         "Images": ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'),
#         "Documents": ('.pdf', '.doc', '.docx', '.csv', '.xls', '.xlsx', '.pptx', '.txt', '.rtf'),
#         "Audio": ('.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'),
#         "Videos": ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'),
#         "Archives": ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'),
#         "Code": ('.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.sh'),
#         "Executables": ('.exe', '.msi', '.dmg', '.pkg', '.deb'),
#         "Others": ()  # Default category
#     }

# class FileLogger:
#     """Handles logging of file operations."""
    
#     def __init__(self, log_file: str = FileOrganizerConfig.LOG_FILE):
#         self.log_file = log_file
#         self.setup_logging()
    
#     def setup_logging(self) -> None:
#         """Initialize or load the log file."""
#         try:
#             if not os.path.exists(self.log_file):
#                 with open(self.log_file, 'w') as f:
#                     json.dump({"moves": [], "errors": []}, f)
#         except Exception as e:
#             logger.error(f"Failed to setup logging: {e}")
    
#     def log_action(self, action_type: str, source: str, destination: Optional[str] = None, error_msg: Optional[str] = None) -> None:
#         """Log file movements and errors."""
#         try:
#             # Read existing data
#             data = {"moves": [], "errors": []}
#             if os.path.exists(self.log_file):
#                 with open(self.log_file, 'r') as f:
#                     data = json.load(f)
            
#             # Add new entry
#             entry = {
#                 "timestamp": datetime.now().strftime(FileOrganizerConfig.DATE_FORMAT),
#                 "source": source,
#                 "destination": destination,
#                 "error": error_msg
#             }
            
#             if action_type not in data:
#                 data[action_type] = []
            
#             data[action_type].append(entry)
            
#             # Write updated data
#             with open(self.log_file, 'w') as f:
#                 json.dump(data, f, indent=4)
                
#         except Exception as e:
#             logger.error(f"Failed to log action: {e}")

# class FileUtils:
#     """Utility functions for file operations."""
#     @staticmethod
#     def is_hidden_file(filename: str)->bool:
#         return filename.startswith(".")
    
#     @staticmethod
#     def get_file_hash(path:str,chunk_size=8193)->str:
#         try:
#             sha256=hashlib.sha256()
#             with open(path,"rb") as f:
#                 for chunk in iter(lambda: f,read(chunk_size),b""):
#                     sha256.update(chunk)
#             return sha256.hexdigest()
#         except Exception as e:
#             return f"ERROR: {e}"

#     @staticmethod
#     def get_unique_filename(destination_path: str) -> str:
#         """Handle duplicate filenames by adding suffixes."""
#         if not os.path.exists(destination_path):
#             return destination_path
            
#         base, ext = os.path.splitext(destination_path)
#         counter = 1
#         original_base = base
        
#         while os.path.exists(destination_path):
#             destination_path = f"{original_base}_{counter}{ext}"
#             counter += 1
            
#         return destination_path
    
#     @staticmethod
#     def get_file_category(filename: str) -> str:
#         """Determine the category of a file based on its extension."""
#         file_ext = os.path.splitext(filename)[1].lower()
        
#         for category, extensions in FileOrganizerConfig.EXTENSIONS_MAPPING.items():
#             if file_ext in extensions:
#                 return category
        
#         return "Others"
    
#     @staticmethod
#     def is_hidden_file(filename: str) -> bool:
#         """Check if a file is hidden."""
#         return filename.startswith('.') or Path(filename).stem.startswith('.')
    
#     @staticmethod
#     def get_file_hash(file_path: str) -> str:
#         """Calculate SHA-256 hash of a file."""
#         sha256 = hashlib.sha256()
#         try:
#             with open(file_path, 'rb') as f:
#                 for block in iter(lambda: f.read(FileOrganizerConfig.HASH_BLOCK_SIZE), b''):
#                     sha256.update(block)
#             return sha256.hexdigest()
#         except Exception as e:
#             return f"ERROR: {e}"
    
#     @staticmethod
#     def format_file_size(size_bytes: int) -> str:
#         """Format file size in human readable format."""
#         if size_bytes < 1024:
#             return f"{size_bytes:,} bytes"
#         elif size_bytes < 1024 * 1024:
#             return f"{size_bytes/1024:.1f} KB"
#         else:
#             return f"{size_bytes/(1024*1024):.1f} MB"

# class FileOrganizer:
#     """Main file organizer class."""
    
#     def __init__(self):
#         self.logger = FileLogger()
#         self.utils = FileUtils()
    
#     def count_files_by_category(self, directory: str, include_hidden: bool = False) -> Dict[str, int]:
#         """Count files in each category for preview."""
#         category_counts = {category: 0 for category in FileOrganizerConfig.EXTENSIONS_MAPPING.keys()}
        
#         try:
#             for dirpath, _, filenames in os.walk(directory):
#                 for filename in filenames:
#                     if not include_hidden and self.utils.is_hidden_file(filename):
#                         continue
                    
#                     category = self.utils.get_file_category(filename)
#                     category_counts[category] += 1
#         except Exception as e:
#             logger.error(f"Error counting files: {e}")
        
#         return category_counts
    
#     def organize_files(self, root_directory: str, flatten_structure: bool = False, 
#                       include_hidden: bool = False, progress_callback: Optional[Callable] = None) -> Tuple[bool, str]:
#         """Organize files recursively with progress tracking."""
#         if not os.path.exists(root_directory):
#             return False, "Directory does not exist."
        
#         # Count total files for progress tracking
#         total_files = self._count_total_files(root_directory, include_hidden)
        
#         if total_files == 0:
#             return False, "No files found in the directory to organize."
        
#         processed_files = 0
#         errors = []
        
#         # Organize files
#         for dirpath, _, filenames in os.walk(root_directory):
#             for filename in filenames:
#                 if not include_hidden and self.utils.is_hidden_file(filename):
#                     continue
                
#                 result = self._move_file(dirpath, filename, root_directory, flatten_structure)
#                 if result['success']:
#                     processed_files += 1
#                 else:
#                     errors.append(result['error'])
                
#                 # Update progress
#                 if progress_callback:
#                     progress_callback(processed_files / total_files)
        
#         # Clean empty directories
#         empty_dirs = self._clean_empty_directories(root_directory, flatten_structure)
        
#         message = f"Processed {processed_files} files, cleaned {empty_dirs} empty directories."
#         if errors:
#             message += f" Encountered {len(errors)} errors."
        
#         return True, message
    
#     def _count_total_files(self, directory: str, include_hidden: bool) -> int:
#         """Count total files in directory."""
#         count = 0
#         try:
#             for dirpath, _, filenames in os.walk(directory):
#                 for filename in filenames:
#                     if not include_hidden and self.utils.is_hidden_file(filename):
#                         continue
#                     count += 1
#         except Exception as e:
#             logger.error(f"Error counting total files: {e}")
#         return count
    
#     def _move_file(self, dirpath: str, filename: str, root_directory: str, flatten_structure: bool) -> Dict:
#         """Move a single file to its category folder."""
#         try:
#             src_path = os.path.join(dirpath, filename)
#             category = self.utils.get_file_category(filename)
            
#             # Set destination path
#             if flatten_structure:
#                 dest_dir = os.path.join(root_directory, category)
#             else:
#                 dest_dir = os.path.join(dirpath, category)
            
#             os.makedirs(dest_dir, exist_ok=True)
#             dest_path = os.path.join(dest_dir, filename)
            
#             # Handle duplicates
#             dest_path = self.utils.get_unique_filename(dest_path)
            
#             # Move file
#             shutil.move(src_path, dest_path)
#             self.logger.log_action("moves", src_path, dest_path)
            
#             return {'success': True, 'error': None}
            
#         except Exception as e:
#             error_msg = f"Failed to move {filename}: {str(e)}"
#             self.logger.log_action("errors", src_path, error_msg=error_msg)
#             return {'success': False, 'error': error_msg}
    
#     def _clean_empty_directories(self, root_directory: str, flatten_structure: bool) -> int:
#         """Clean empty directories after organization."""
#         empty_dirs = 0
#         try:
#             for dirpath, dirnames, filenames in list(os.walk(root_directory, topdown=False)):
#                 # Skip root directory and category directories if flattening
#                 if dirpath == root_directory:
#                     continue
                
#                 if flatten_structure and os.path.basename(dirpath) in FileOrganizerConfig.EXTENSIONS_MAPPING.keys():
#                     continue
                
#                 try:
#                     if not os.listdir(dirpath):
#                         os.rmdir(dirpath)
#                         empty_dirs += 1
#                 except OSError as e:
#                     error_msg = f"Failed to remove empty directory {dirpath}: {str(e)}"
#                     self.logger.log_action("errors", dirpath, error_msg=error_msg)
#         except Exception as e:
#             logger.error(f"Error cleaning directories: {e}")
        
#         return empty_dirs
    
#     def undo_last_organization(self) -> Tuple[bool, str]:
#         """Revert the last organization using the log file."""
#         try:
#             if not os.path.exists(self.logger.log_file):
#                 return False, "No log file found - nothing to undo."
            
#             with open(self.logger.log_file, 'r') as f:
#                 data = json.load(f)
            
#             if not data.get("moves"):
#                 return False, "No previous organization actions found to undo."
            
#             undone_count = 0
#             errors = []
#             remaining_moves = []
            
#             # Undo moves in reverse order
#             for move in reversed(data["moves"]):
#                 try:
#                     if os.path.exists(move["destination"]):
#                         os.makedirs(os.path.dirname(move["source"]), exist_ok=True)
#                         shutil.move(move["destination"], move["source"])
#                         undone_count += 1
#                     else:
#                         errors.append(f"Destination file not found: {move['destination']}")
#                         remaining_moves.append(move)
#                 except Exception as e:
#                     errors.append(f"Failed to undo {move['destination']}: {str(e)}")
#                     remaining_moves.append(move)
            
#             # Update log file
#             data["moves"] = remaining_moves
#             with open(self.logger.log_file, 'w') as f:
#                 json.dump(data, f, indent=4)
            
#             message = f"Successfully undone {undone_count} file moves."
#             if errors:
#                 message += f" {len(errors)} errors occurred."
            
#             return True, message
            
#         except Exception as e:
#             logger.error(f"Error during undo: {e}")
#             return False, f"Error during undo operation: {str(e)}"
    
#     # def find_duplicates(self, directory: str, include_hidden: bool = False) -> Dict[str, List[str]]:
#         """Find duplicate files based on SHA-256 hash."""
#         hash_map = {}
#         duplicates = {}
        
#         try:
#             for dirpath, _, filenames in os.scandir(directory):
#                 for filename in filenames:
#                     if not include_hidden and self.utils.is_hidden_file(filename):
#                         continue
                    
#                     file_path = os.path.join(dirpath, filename)
                    
#                     if os.path.isdir(file_path):
#                         continue
                    
#                     file_hash = self.utils.get_file_hash(file_path)
#                     if file_hash.startswith("ERROR"):
#                         self.logger.log_action("errors", file_path, error_msg=f"Hashing failed: {file_hash}")
#                         continue
                    
#                     if file_hash in hash_map:
#                         if file_hash not in duplicates:
#                             duplicates[file_hash] = [hash_map[file_hash]]
#                         duplicates[file_hash].append(file_path)
#                     else:
#                         hash_map[file_hash] = file_path
                        
#         except Exception as e:
#             logger.error(f"Error finding duplicates: {e}")
        
#         return duplicates
    
#     def find_duplicates(self, directory: str, include_hidden: bool = False):
#         from collections import defaultdict
#         from concurrent.futures import ThreadPoolExecutor

#         duplicates = defaultdict(list)
#         hash_map = {}

#         try:
#             files = list(self._all_files(directory, include_hidden))

#             def process_file(path):
#                 return (path, self.utils.get_file_hash(path))

#             with ThreadPoolExecutor() as executor:
#                 for path, file_hash in executor.map(process_file, files):
#                     if file_hash.startswith("ERROR"):
#                         self.logger.log_action("errors", path, error_msg=f"Hashing failed: {file_hash}")
#                         continue

#                     if file_hash in hash_map:
#                         duplicates[file_hash].append(path)
#                         if len(duplicates[file_hash]) == 1:
#                             duplicates[file_hash].append(hash_map[file_hash])
#                     else:
#                         hash_map[file_hash] = path

#         except Exception as e:
#             self.logger.log_action("errors", directory, error_msg=f"Error finding duplicates: {e}")

#         return {k: list(set(v)) for k, v in duplicates.items()}

# class StreamlitUI:
#     """Streamlit user interface for the file organizer."""
    
#     def __init__(self):
#         self.organizer = FileOrganizer()
#         self.utils = FileUtils()
#         self._setup_page_config()
#         self._apply_custom_styling()
    
#     def _setup_page_config(self):
#         """Configure Streamlit page settings."""
#         st.set_page_config(
#             page_title="File Organizer",
#             page_icon="📁",
#             layout="wide",
#             initial_sidebar_state="expanded"
#         )
    
#     def _apply_custom_styling(self):
#         """Apply custom CSS styling."""
#         st.markdown("""
#         <style>
#             .stApp {
#                 background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);
#             }
            
#             .main .block-container {
#                 background: rgba(255, 255, 255, 0.9);
#                 backdrop-filter: blur(10px);
#                 border-radius: 20px;
#                 padding: 2rem;
#                 margin: 1rem;
#                 box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
#             }
            
#             h1 {
#                 color: #2c3f50;
#                 font-weight: 700;
#                 text-align: center;
#                 margin-bottom: 0.5rem;
#                 background: linear-gradient(90deg, #4ca1af, #3a6073);
#                 -webkit-background-clip: text;
#                 -webkit-text-fill-color: transparent;
#                 background-clip: text;
#             }
            
#             .stButton > button {
#                 background: linear-gradient(45deg, #667eea, #764ba2);
#                 color: white;
#                 border: none;
#                 border-radius: 10px;
#                 padding: 0.6rem 1.2rem;
#                 font-weight: 600;
#                 transition: all 0.3s ease;
#                 box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
#             }
            
#             .stButton > button:hover {
#                 transform: translateY(-2px);
#                 box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
#             }
            
#             .success-box {
#                 background: rgba(46, 204, 113, 0.1);
#                 border: 2px solid #2ecc71;
#                 border-radius: 15px;
#                 padding: 1.5rem;
#                 text-align: center;
#                 margin: 1rem 0;
#             }
            
#             .error-box {
#                 background: rgba(231, 76, 60, 0.1);
#                 border: 2px solid #e74c3c;
#                 border-radius: 15px;
#                 padding: 1.5rem;
#                 text-align: center;
#                 margin: 1rem 0;
#             }
#         </style>
#         """, unsafe_allow_html=True)
    
#     def render_header(self):
#         """Render the main header."""
#         st.title("📊 Professional File Organizer")
#         st.markdown("""
#         <div style='text-align: center; margin-bottom: 2rem;'>
#             <p style='font-size: 1.2rem; color: #7f8c8d; font-weight: 500;'>
#                 Enterprise-grade file organization solution with advanced analytics
#             </p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     def render_sidebar(self) -> Tuple[str, bool, bool]:
#         """Render the sidebar configuration panel."""
#         with st.sidebar:
#             st.markdown("### ⚙️ Configuration Panel")
            
#             # Directory selection
#             st.markdown("#### 📂 Directory Selection")
#             folder_path = st.text_input(
#                 "Target Directory Path:",
#                 placeholder="e.g., C:\\Users\\Documents or /home/user/documents",
#                 help="Enter the absolute path to the directory you want to organize"
#             )
            
#             # Organization options
#             st.markdown("#### 🔧 Organization Settings")
#             flatten_structure = st.checkbox(
#                 "Enable Directory Flattening",
#                 help="Consolidate all files into category folders at the root level"
#             )
            
#             # Advanced options
#             with st.expander("🔬 Advanced Options"):
#                 show_hidden = st.checkbox("Include Hidden Files", value=False)
#                 st.info("💡 All file movements are automatically logged for rollback capability.")
            
#             # Directory analysis
#             if folder_path and os.path.exists(folder_path):
#                 self._render_directory_analysis(folder_path, show_hidden)
        
#         return folder_path, flatten_structure, show_hidden
    
#     def _render_directory_analysis(self, folder_path: str, include_hidden: bool):
#         """Render directory analysis in sidebar."""
#         st.markdown("#### 📊 Directory Analysis")
        
#         try:
#             with st.spinner("Analyzing directory..."):
#                 category_counts = self.organizer.count_files_by_category(folder_path, include_hidden)
            
#             total_files = sum(category_counts.values())
#             st.metric("Total Files", f"{total_files:,}")
            
#             if total_files > 0:
#                 st.markdown("**File Distribution:**")
#                 for category, count in category_counts.items():
#                     if count > 0:
#                         percentage = (count / total_files * 100)
#                         st.markdown(f"""
#                         <div style='
#                             background: rgba(102, 126, 234, 0.1);
#                             padding: 0.5rem;
#                             margin: 0.3rem 0;
#                             border-radius: 8px;
#                             border-left: 4px solid #667eea;
#                         '>
#                             <strong>{category}:</strong> {count:,} files ({percentage:.1f}%)
#                         </div>
#                         """, unsafe_allow_html=True)
            
#             # Duplicate detection
#             st.markdown("#### 🔍 Duplicate Analysis")
#             with st.spinner("Scanning for duplicates..."):
#                 duplicates = self.organizer.find_duplicates(folder_path, include_hidden)
            
#             if duplicates:
#                 total_duplicates = sum(len(files) - 1 for files in duplicates.values())
#                 st.warning(f"Found **{total_duplicates}** duplicate files in **{len(duplicates)}** groups.")
                
#                 with st.expander("View Duplicate Details"):
#                     for hash_val, file_list in duplicates.items():
#                         st.markdown(f"**Group ({len(file_list)} files):**")
#                         for file_path in file_list:
#                             st.text(f"  • {file_path}")
#                         st.markdown("---")
#             else:
#                 st.success("No duplicate files found!")
                
#         except Exception as e:
#             st.error(f"Error analyzing directory: {str(e)}")
    
#     def render_main_content(self, folder_path: str):
#         """Render the main content area."""
#         col1, col2 = st.columns([3, 1])
        
#         with col1:
#             if folder_path:
#                 if os.path.exists(folder_path):
#                     st.success(f"✅ **Directory Validated:** `{folder_path}`")
#                     self._render_directory_preview(folder_path)
#                 elif folder_path.strip():
#                     st.error("❌ **Directory Not Found:** Please verify the path exists.")
#             else:
#                 st.info("👆 Please enter a directory path in the configuration panel.")
        
#         with col2:
#             return self._render_control_panel(folder_path)
    
#     def _render_directory_preview(self, folder_path: str):
#         """Render directory structure preview."""
#         with st.expander("📋 Directory Structure Preview", expanded=False):
#             try:
#                 items = sorted(os.listdir(folder_path))[:25]
#                 if items:
#                     preview_col1, preview_col2 = st.columns(2)
                    
#                     for i, item in enumerate(items):
#                         item_path = os.path.join(folder_path, item)
#                         target_col = preview_col1 if i % 2 == 0 else preview_col2
                        
#                         with target_col:
#                             if os.path.isdir(item_path):
#                                 st.markdown(f"📁 **{item}/**")
#                             else:
#                                 try:
#                                     file_size = os.path.getsize(item_path)
#                                     size_str = self.utils.format_file_size(file_size)
#                                     st.markdown(f"📄 {item} ({size_str})")
#                                 except Exception:
#                                     st.markdown(f"📄 {item} (size unknown)")
                    
#                     total_items = len(os.listdir(folder_path))
#                     if total_items > 25:
#                         st.info(f"... and {total_items - 25} more items")
#                 else:
#                     st.info("📭 Directory is empty")
                    
#             except PermissionError:
#                 st.error("🚫 Access denied: Insufficient permissions.")
#             except Exception as e:
#                 st.error(f"⚠️ Error accessing directory: {str(e)}")
    
#     def _render_control_panel(self, folder_path: str) -> Tuple[bool, bool]:
#         """Render the control panel."""
#         st.markdown("### 🚀 Control Panel")
        
#         # Status indicator
#         if folder_path and os.path.exists(folder_path):
#             st.markdown("""
#             <div class='success-box'>
#                 <strong style='color: #27ae60;'>🟢 READY</strong><br>
#                 <small>System ready for organization</small>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div style='
#                 background: rgba(243, 156, 18, 0.1);
#                 border: 1px solid #f39c12;
#                 border-radius: 10px;
#                 padding: 1rem;
#                 text-align: center;
#                 margin-bottom: 1rem;
#             '>
#                 <strong style='color: #e67e22;'>🟡 STANDBY</strong><br>
#                 <small>Awaiting directory selection</small>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # Action buttons
#         organize_button = st.button(
#             "🗂️ Execute Organization",
#             type="primary",
#             disabled=not (folder_path and os.path.exists(folder_path)),
#             use_container_width=True,
#             help="Begin automated file organization process"
#         )
        
#         undo_button = st.button(
#             "↩️ Rollback Changes",
#             use_container_width=True,
#             help="Revert the most recent organization operation"
#         )
        
#         return organize_button, undo_button
    
#     def handle_organization(self, folder_path: str, flatten_structure: bool, show_hidden: bool):
#         """Handle the organization process."""
#         if not folder_path or not os.path.exists(folder_path):
#             st.error("🚫 **Operation Failed:** Please select a valid directory first.")
#             return
        
#         st.markdown("### 🔄 Organization in Progress")
        
#         progress_bar = st.progress(0)
#         status_text = st.empty()
#         start_time = time.time()
        
#         def update_progress(progress):
#             progress_bar.progress(progress)
#             elapsed = time.time() - start_time
#             status_text.markdown(f"""
#             <div style='
#                 background: rgba(102, 126, 234, 0.1);
#                 padding: 1rem;
#                 border-radius: 10px;
#                 text-align: center;
#             '>
#                 <strong>Processing:</strong> {int(progress * 100)}% Complete<br>
#                 <small>Elapsed Time: {elapsed:.1f}s</small>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # Execute organization
#         success, message = self.organizer.organize_files(
#             folder_path, flatten_structure, show_hidden, update_progress
#         )
        
#         # Show results
#         progress_bar.progress(100)
#         total_time = time.time() - start_time
        
#         if success:
#             st.markdown(f"""
#             <div class='success-box'>
#                 <h3 style='color: #27ae60; margin: 0;'>✅ Operation Successful</h3>
#                 <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{message}</p>
#                 <small style='color: #7f8c8d;'>Completed in {total_time:.2f} seconds</small>
#             </div>
#             """, unsafe_allow_html=True)
#             st.balloons()
#         else:
#             st.markdown(f"""
#             <div class='error-box'>
#                 <h3 style='color: #c0392b; margin: 0;'>❌ Operation Failed</h3>
#                 <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{message}</p>
#                 <small style='color: #7f8c8d;'>Duration: {total_time:.2f} seconds</small>
#             </div>
#             """, unsafe_allow_html=True)
    
#     def handle_undo(self):
#         """Handle the undo operation."""
#         st.markdown("### ↩️ Rollback Operation")
        
#         with st.spinner("Executing rollback procedure..."):
#             success, message = self.organizer.undo_last_organization()
        
#         if success:
#             st.markdown(f"""
#             <div style='
#                 background: rgba(52, 152, 219, 0.1);
#                 border: 2px solid #3498db;
#                 border-radius: 15px;
#                 padding: 1.5rem;
#                 text-align: center;
#                 margin: 1rem 0;
#             '>
#                 <h3 style='color: #2980b9; margin: 0;'>✅ Rollback Successful</h3>
#                 <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{message}</p>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div style='
#                 background: rgba(243, 156, 18, 0.1);
#                 border: 2px solid #f39c12;
#                 border-radius: 15px;
#                 padding: 1.5rem;
#                 text-align: center;
#                 margin: 1rem 0;
#             '>
#                 <h3 style='color: #e67e22; margin: 0;'>⚠️ Rollback Notice</h3>
#                 <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{message}</p>
#             </div>
#             """, unsafe_allow_html=True)
    
#     def run(self):
#         """Main application entry point."""
#         self.render_header()
        
#         # Get configuration from sidebar
#         folder_path, flatten_structure, show_hidden = self.render_sidebar()
        
#         # Render main content and get button states
#         organize_button, undo_button = self.render_main_content(folder_path)
        
#         # Handle button actions
#         if organize_button:
#             self.handle_organization(folder_path, flatten_structure, show_hidden)
        
#         if undo_button:
#             self.handle_undo()
        
#         # Footer
#         st.markdown("---")
#         st.markdown("""
#             <div style='text-align: center; padding-top: 1rem;'>
#                 <p style='font-size: 0.9rem; color: #7f8c8d;'>
#                     Developed with ❤️ for efficient file management.
#                 </p>
#             </div>
#         """, unsafe_allow_html=True)

# def main():
#     """Application entry point."""
#     try:
#         app = StreamlitUI()
#         app.run()
#     except Exception as e:
#         st.error(f"Application error: {str(e)}")
#         logger.error(f"Application error: {e}")

# if __name__ == "__main__":
#     main()