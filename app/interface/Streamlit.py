import streamlit as st
import os

from datetime import datetime
from pathlib import Path
import time

from scripts.FileOrganizer import FileOrganizer
from core.FileUtils import FileUtils

from typing import Tuple


class StreamlitUI:
    """Streamlit user interface for the file organizer."""
    
    def __init__(self):
        self.organizer = FileOrganizer()
        self.utils = FileUtils()
        self._setup_page_config()
        self._apply_custom_styling()
    
    def _setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="File Organizer",
            page_icon="📁",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def _apply_custom_styling(self):
        """Apply custom CSS styling."""
        st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);
            }
            
            .main .block-container {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 2rem;
                margin: 1rem;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            }
            
            h1 {
                color: #2c3f50;
                font-weight: 700;
                text-align: center;
                margin-bottom: 0.5rem;
                background: linear-gradient(90deg, #4ca1af, #3a6073);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .stButton > button {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.6rem 1.2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .success-box {
                background: rgba(46, 204, 113, 0.1);
                border: 2px solid #2ecc71;
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                margin: 1rem 0;
            }
            
            .error-box {
                background: rgba(231, 76, 60, 0.1);
                border: 2px solid #e74c3c;
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                margin: 1rem 0;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render the main header."""
        st.title("📊 Professional File Organizer")
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <p style='font-size: 1.2rem; color: #7f8c8d; font-weight: 500;'>
                Enterprise-grade file organization solution with advanced analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self) -> Tuple[str, bool, bool]:
        """Render the sidebar configuration panel."""
        with st.sidebar:
            st.markdown("### ⚙️ Configuration Panel")
            
            # Directory selection
            st.markdown("#### 📂 Directory Selection")
            folder_path = st.text_input(
                "Target Directory Path:",
                placeholder="e.g., C:\\Users\\Documents or /home/user/documents",
                help="Enter the absolute path to the directory you want to organize"
            )
            
            # Organization options
            st.markdown("#### 🔧 Organization Settings")
            flatten_structure = st.checkbox(
                "Enable Directory Flattening",
                help="Consolidate all files into category folders at the root level"
            )
            
            # Advanced options
            with st.expander("🔬 Advanced Options"):
                show_hidden = st.checkbox("Include Hidden Files", value=False)
                st.info("💡 All file movements are automatically logged for rollback capability.")
            
            # Directory analysis
            if folder_path and os.path.exists(folder_path):
                self._render_directory_analysis(folder_path, show_hidden)
        
        return folder_path, flatten_structure, show_hidden
    
    def _render_directory_analysis(self, folder_path: str, include_hidden: bool):
        """Render directory analysis in sidebar."""
        st.markdown("#### 📊 Directory Analysis")
        
        try:
            with st.spinner("Analyzing directory..."):
                category_counts = self.organizer.count_files_by_category(folder_path, include_hidden)
            
            total_files = sum(category_counts.values())
            st.metric("Total Files", f"{total_files:,}")
            
            if total_files > 0:
                st.markdown("**File Distribution:**")
                for category, count in category_counts.items():
                    if count > 0:
                        percentage = (count / total_files * 100)
                        st.markdown(f"""
                        <div style='
                            background: rgba(102, 126, 234, 0.1);
                            padding: 0.5rem;
                            margin: 0.3rem 0;
                            border-radius: 8px;
                            border-left: 4px solid #667eea;
                        '>
                            <strong>{category}:</strong> {count:,} files ({percentage:.1f}%)
                        </div>
                        """, unsafe_allow_html=True)
            
            # Duplicate detection
            st.markdown("#### 🔍 Duplicate Analysis")
            with st.spinner("Scanning for duplicates..."):
                duplicates = self.organizer.find_duplicates(folder_path, include_hidden)
            
            if duplicates:
                total_duplicates = sum(len(files) - 1 for files in duplicates.values())
                st.warning(f"Found **{total_duplicates}** duplicate files in **{len(duplicates)}** groups.")
                
                with st.expander("View Duplicate Details"):
                    for hash_val, file_list in duplicates.items():
                        st.markdown(f"**Group ({len(file_list)} files):**")
                        for file_path in file_list:
                            st.text(f"  • {file_path}")
                        st.markdown("---")
            else:
                st.success("No duplicate files found!")
                
        except Exception as e:
            st.error(f"Error analyzing directory: {str(e)}")
    
    def render_main_content(self, folder_path: str):
        """Render the main content area."""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if folder_path:
                if os.path.exists(folder_path):
                    st.success(f"✅ **Directory Validated:** `{folder_path}`")
                    self._render_directory_preview(folder_path)
                elif folder_path.strip():
                    st.error("❌ **Directory Not Found:** Please verify the path exists.")
            else:
                st.info("👆 Please enter a directory path in the configuration panel.")
        
        with col2:
            return self._render_control_panel(folder_path)
    
    def _render_directory_preview(self, folder_path: str):
        """Render directory structure preview."""
        with st.expander("📋 Directory Structure Preview", expanded=False):
            try:
                items = sorted(os.listdir(folder_path))[:25]
                if items:
                    preview_col1, preview_col2 = st.columns(2)
                    
                    for i, item in enumerate(items):
                        item_path = os.path.join(folder_path, item)
                        target_col = preview_col1 if i % 2 == 0 else preview_col2
                        
                        with target_col:
                            if os.path.isdir(item_path):
                                st.markdown(f"📁 **{item}/**")
                            else:
                                try:
                                    file_size = os.path.getsize(item_path)
                                    size_str = self.utils.format_file_size(file_size)
                                    st.markdown(f"📄 {item} ({size_str})")
                                except Exception:
                                    st.markdown(f"📄 {item} (size unknown)")
                    
                    total_items = len(os.listdir(folder_path))
                    if total_items > 25:
                        st.info(f"... and {total_items - 25} more items")
                else:
                    st.info("📭 Directory is empty")
                    
            except PermissionError:
                st.error("🚫 Access denied: Insufficient permissions.")
            except Exception as e:
                st.error(f"⚠️ Error accessing directory: {str(e)}")
    
    def _render_control_panel(self, folder_path: str) -> Tuple[bool, bool]:
        """Render the control panel."""
        st.markdown("### 🚀 Control Panel")
        
        # Status indicator
        if folder_path and os.path.exists(folder_path):
            st.markdown("""
            <div class='success-box'>
                <strong style='color: #27ae60;'>🟢 READY</strong><br>
                <small>System ready for organization</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='
                background: rgba(243, 156, 18, 0.1);
                border: 1px solid #f39c12;
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
                margin-bottom: 1rem;
            '>
                <strong style='color: #e67e22;'>🟡 STANDBY</strong><br>
                <small>Awaiting directory selection</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        organize_button = st.button(
            "🗂️ Execute Organization",
            type="primary",
            disabled=not (folder_path and os.path.exists(folder_path)),
            use_container_width=True,
            help="Begin automated file organization process"
        )
        
        undo_button = st.button(
            "↩️ Rollback Changes",
            use_container_width=True,
            help="Revert the most recent organization operation"
        )
        
        return organize_button, undo_button
    
    def handle_organization(self, folder_path: str, flatten_structure: bool, show_hidden: bool):
        """Handle the organization process."""
        if not folder_path or not os.path.exists(folder_path):
            st.error("🚫 **Operation Failed:** Please select a valid directory first.")
            return
        
        st.markdown("### 🔄 Organization in Progress")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        start_time = time.time()
        
        def update_progress(progress):
            progress_bar.progress(progress)
            elapsed = time.time() - start_time
            status_text.markdown(f"""
            <div style='
                background: rgba(102, 126, 234, 0.1);
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
            '>
                <strong>Processing:</strong> {int(progress * 100)}% Complete<br>
                <small>Elapsed Time: {elapsed:.1f}s</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Execute organization
        success, message = self.organizer.organize_files(
            folder_path, flatten_structure, show_hidden, update_progress
        )
        
        # Show results
        progress_bar.progress(100)
        total_time = time.time() - start_time
        
        if success:
            st.markdown(f"""
            <div class='success-box'>
                <h3 style='color: #27ae60; margin: 0;'>✅ Operation Successful</h3>
                <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{message}</p>
                <small style='color: #7f8c8d;'>Completed in {total_time:.2f} seconds</small>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown(f"""
            <div class='error-box'>
                <h3 style='color: #c0392b; margin: 0;'>❌ Operation Failed</h3>
                <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{message}</p>
                <small style='color: #7f8c8d;'>Duration: {total_time:.2f} seconds</small>
            </div>
            """, unsafe_allow_html=True)
    
    def handle_undo(self):
        """Handle the undo operation."""
        st.markdown("### ↩️ Rollback Operation")
        
        with st.spinner("Executing rollback procedure..."):
            success, message = self.organizer.undo_last_organization()
        
        if success:
            st.markdown(f"""
            <div style='
                background: rgba(52, 152, 219, 0.1);
                border: 2px solid #3498db;
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                margin: 1rem 0;
            '>
                <h3 style='color: #2980b9; margin: 0;'>✅ Rollback Successful</h3>
                <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{message}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='
                background: rgba(243, 156, 18, 0.1);
                border: 2px solid #f39c12;
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                margin: 1rem 0;
            '>
                <h3 style='color: #e67e22; margin: 0;'>⚠️ Rollback Notice</h3>
                <p style='margin: 0.5rem 0; font-size: 1.1rem;'>{message}</p>
            </div>
            """, unsafe_allow_html=True)
    
    def run(self):
        """Main application entry point."""
        self.render_header()
        
        # Get configuration from sidebar
        folder_path, flatten_structure, show_hidden = self.render_sidebar()
        
        # Render main content and get button states
        organize_button, undo_button = self.render_main_content(folder_path)
        
        # Handle button actions
        if organize_button:
            self.handle_organization(folder_path, flatten_structure, show_hidden)
        
        if undo_button:
            self.handle_undo()
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; padding-top: 1rem;'>
                <p style='font-size: 0.9rem; color: #7f8c8d;'>
                    Developed with ❤️ for efficient file management.
                </p>
            </div>
        """, unsafe_allow_html=True)
