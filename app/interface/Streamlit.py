import streamlit as st
import os

from datetime import datetime
from pathlib import Path
import time

from scripts.FileOrganizer import FileOrganizer
from app.core.FileUtils import FileUtils
from app.core.FileAnalyzer import FileAnalyzer
from app.core.SecurityManager import SecurityManager
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from typing import Tuple


class StreamlitUI:
    """Streamlit user interface for the file organizer."""
    
    def __init__(self):
        self.organizer = FileOrganizer()
        self.utils = FileUtils()
        self.analyzer = FileAnalyzer()
        self.security = SecurityManager()
        self._setup_page_config()
        self._apply_custom_styling()
    
    def _setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Enterprise File Organizer",
            page_icon="🗂️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def _apply_custom_styling(self):
        """Apply professional custom CSS styling."""
        st.markdown("""
        <style>
            /* Global App Styling */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            /* Main Container */
            .main .block-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(15px);
                border-radius: 16px;
                padding: 2.5rem;
                margin: 1rem;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.08),
                    0 0 0 1px rgba(255, 255, 255, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            /* Header Styling */
            h1 {
                color: #1a202c;
                font-weight: 800;
                text-align: center;
                margin-bottom: 0.5rem;
                font-size: 2.5rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            h2 {
                color: #2d3748;
                font-weight: 700;
                margin-top: 2rem;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 3px solid #e2e8f0;
                position: relative;
            }
            
            h2:before {
                content: '';
                position: absolute;
                bottom: -3px;
                left: 0;
                width: 60px;
                height: 3px;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 2px;
            }
            
            h3 {
                color: #4a5568;
                font-weight: 600;
                margin-bottom: 1rem;
            }
            
            /* Button Styling */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                font-size: 0.95rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 
                    0 4px 12px rgba(102, 126, 234, 0.25),
                    0 0 0 1px rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 
                    0 8px 25px rgba(102, 126, 234, 0.35),
                    0 0 0 1px rgba(255, 255, 255, 0.2);
                background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
            }
            
            .stButton > button:active {
                transform: translateY(0px);
                transition: all 0.1s;
            }
            
            /* Card Components */
            .metric-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 1.5rem;
                margin: 0.5rem 0;
                box-shadow: 
                    0 4px 12px rgba(0, 0, 0, 0.04),
                    0 0 0 1px rgba(255, 255, 255, 0.5);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 
                    0 8px 25px rgba(0, 0, 0, 0.08),
                    0 0 0 1px rgba(255, 255, 255, 0.6);
            }
            
            .status-card {
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                margin: 1rem 0;
                position: relative;
                overflow: hidden;
            }
            
            .status-ready {
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                color: white;
                box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
            }
            
            .status-standby {
                background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
                color: white;
                box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3);
            }
            
            .status-error {
                background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
                color: white;
                box-shadow: 0 4px 12px rgba(245, 101, 101, 0.3);
            }
            
            /* Success/Error Messages */
            .success-alert {
                background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
                border: 2px solid #9ae6b4;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                color: #1a202c;
                box-shadow: 0 4px 12px rgba(154, 230, 180, 0.2);
            }
            
            .error-alert {
                background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
                border: 2px solid #fc8181;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                color: #1a202c;
                box-shadow: 0 4px 12px rgba(252, 129, 129, 0.2);
            }
            
            .warning-alert {
                background: linear-gradient(135deg, #fefcbf 0%, #faf089 100%);
                border: 2px solid #f6e05e;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                color: #1a202c;
                box-shadow: 0 4px 12px rgba(246, 224, 94, 0.2);
            }
            
            .info-alert {
                background: linear-gradient(135deg, #bee3f8 0%, #90cdf4 100%);
                border: 2px solid #63b3ed;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                color: #1a202c;
                box-shadow: 0 4px 12px rgba(99, 179, 237, 0.2);
            }
            
            /* Sidebar Styling */
            .css-1d391kg {
                background: linear-gradient(180deg, #ffffff 0%, #f7fafc 100%);
                border-right: 1px solid #e2e8f0;
            }
            
            /* Input Fields */
            .stTextInput > div > div > input {
                border-radius: 8px;
                border: 2px solid #e2e8f0;
                padding: 0.75rem;
                font-size: 0.95rem;
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            /* Progress Bar */
            .stProgress > div > div > div {
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 10px;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                border-radius: 8px;
                border: 1px solid #cbd5e0;
            }
            
            /* Metrics */
            [data-testid="metric-container"] {
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                border: 1px solid #e2e8f0;
                padding: 1rem;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            }
            
            /* Footer */
            .footer {
                background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
                color: #e2e8f0;
                padding: 2rem;
                margin-top: 3rem;
                border-radius: 16px;
                text-align: center;
            }
            
            /* Custom Icons */
            .icon-badge {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 0.5rem;
                border-radius: 50%;
                margin-right: 0.5rem;
                font-size: 1.2rem;
                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
            }
            
            /* File Item Styling */
            .file-item {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0.75rem;
                margin: 0.25rem 0;
                transition: all 0.2s ease;
            }
            
            .file-item:hover {
                background: #edf2f7;
                border-color: #cbd5e0;
                transform: translateX(4px);
            }
            
            /* Animation Classes */
            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .slide-in {
                animation: slideInUp 0.5s ease-out;
            }
            
            /* Scrollbar Styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
            }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render the professional main header."""
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1>🗂️ Enterprise File Organizer</h1>
            <p style='font-size: 1.2rem; color: #718096; font-weight: 500; margin-top: -0.5rem;'>
                Advanced file management solution with intelligent organization and analytics
            </p>
            <div style='width: 100px; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); 
                        margin: 1rem auto; border-radius: 2px;'></div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_analysis(self, directory: str):
        """Render enhanced analysis and reports section."""
        st.markdown("## 📊 Storage Analytics Dashboard")
        
        # Create tabs for different analytics
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Storage Usage", "📋 File Distribution", "⏰ Age Analysis", "💾 Space Report"])
        
        with tab1:
            st.markdown("### Storage Usage by Category")
            storage_usage = self.analyzer.analyze_storage_usage(directory)
            
            if storage_usage:
                # Create two columns for chart and summary
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    usage_df = pd.DataFrame([
                        {'Category': cat, 'Size': float(size.split()[0])} 
                        for cat, size in storage_usage.items()
                    ])
                    
                    fig_storage = px.pie(
                        usage_df, 
                        values='Size', 
                        names='Category',
                        title='Storage Distribution',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_storage.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        title_font_size=16
                    )
                    st.plotly_chart(fig_storage, use_container_width=True)
                
                with col2:
                    st.markdown("#### Summary")
                    total_size = sum(float(size.split()[0]) for size in storage_usage.values())
                    
                    for cat, size in storage_usage.items():
                        size_val = float(size.split()[0])
                        percentage = (size_val / total_size * 100) if total_size > 0 else 0
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong style="color: #4a5568;">{cat}</strong><br>
                            <span style="font-size: 1.1rem; color: #2d3748;">{size}</span><br>
                            <small style="color: #718096;">{percentage:.1f}% of total</small>
                        </div>
                        """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### File Distribution Analysis")
            distribution = self.analyzer.get_file_distribution(directory)
            
            if distribution:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    dist_df = pd.DataFrame([
                        {'Category': cat, 'Count': count}
                        for cat, count in distribution.items()
                    ])
                    
                    fig_dist = px.bar(
                        dist_df, 
                        x='Category', 
                        y='Count',
                        title='Number of Files by Category',
                        color='Count',
                        color_continuous_scale='Viridis'
                    )
                    fig_dist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                with col2:
                    st.markdown("#### File Counts")
                    total_files = sum(distribution.values())
                    
                    for cat, count in distribution.items():
                        percentage = (count / total_files * 100) if total_files > 0 else 0
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong style="color: #4a5568;">{cat}</strong><br>
                            <span style="font-size: 1.4rem; color: #2d3748;">{count:,}</span><br>
                            <small style="color: #718096;">{percentage:.1f}% of files</small>
                        </div>
                        """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### File Age Distribution")
            age_dist = self.analyzer.get_age_distribution(directory)
            
            if age_dist:
                age_df = pd.DataFrame([
                    {'Age Range': age, 'Count': len(files)}
                    for age, files in age_dist.items()
                ])
                
                fig_age = px.bar(
                    age_df, 
                    x='Age Range', 
                    y='Count',
                    title='Files by Age Range',
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig_age.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_age, use_container_width=True)
        
        with tab4:
            st.markdown("### Disk Space Report")
            space_report = self.analyzer.generate_disk_space_report(directory)
            
            if space_report:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: center;">
                        <h3 style="color: #667eea; margin: 0;">Total Space Used</h3>
                        <div style="font-size: 2rem; font-weight: bold; color: #2d3748; margin: 0.5rem 0;">
                            {space_report.get('total_space', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("#### Largest Files")
                    largest_files = space_report.get('largest_files', {})
                    
                    for i, (file_path, size) in enumerate(largest_files.items()):
                        if i < 5:  # Show top 5
                            filename = os.path.basename(file_path)
                            st.markdown(f"""
                            <div class="file-item">
                                <strong>{filename}</strong><br>
                                <small style="color: #718096;">{size}</small>
                            </div>
                            """, unsafe_allow_html=True)
    
    def render_sidebar(self) -> Tuple[str, bool, bool]:
        """Render the enhanced sidebar configuration panel."""
        with st.sidebar:
            st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h2 style='color: #2d3748; margin: 0;'>⚙️ Control Panel</h2>
                <p style='color: #718096; font-size: 0.9rem; margin: 0.5rem 0;'>Configure your organization settings</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Directory selection
            st.markdown("#### 📂 Directory Selection")
            folder_path = st.text_input(
                "Target Directory Path:",
                placeholder="Enter full path (e.g., C:\\Users\\Documents)",
                help="Specify the complete path to the directory you want to organize",
                key="folder_input"
            )
            
            if folder_path:
                if os.path.exists(folder_path):
                    st.markdown("""
                    <div class="success-alert" style="padding: 0.75rem; margin: 0.5rem 0;">
                        ✅ <strong>Valid Directory</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="error-alert" style="padding: 0.75rem; margin: 0.5rem 0;">
                        ❌ <strong>Directory Not Found</strong>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Organization options
            st.markdown("#### 🔧 Organization Settings")
            
            flatten_structure = st.checkbox(
                "📁 Enable Directory Flattening",
                help="Move all files to category folders at the root level"
            )
            
            # Advanced options
            with st.expander("🔬 Advanced Configuration"):
                show_hidden = st.checkbox("👁️ Include Hidden Files", value=False)
                st.markdown("""
                <div class="info-alert" style="padding: 0.75rem; margin: 0.5rem 0;">
                    💡 <strong>Note:</strong> All operations are logged for rollback capability
                </div>
                """, unsafe_allow_html=True)
            
            # Directory analysis
            if folder_path and os.path.exists(folder_path):
                st.markdown("---")
                self._render_directory_analysis(folder_path, show_hidden)
        
        return folder_path, flatten_structure, show_hidden
    
    def _render_directory_analysis(self, folder_path: str, include_hidden: bool):
        """Render enhanced directory analysis in sidebar."""
        st.markdown("#### 📊 Directory Insights")
        
        try:
            with st.spinner("Analyzing directory structure..."):
                category_counts = self.organizer.count_files_by_category(folder_path, include_hidden)
            
            total_files = sum(category_counts.values())
            
            # Total files metric
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; margin: 1rem 0;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{total_files:,}</div>
                <div style="color: #718096; font-size: 0.9rem;">Total Files</div>
            </div>
            """, unsafe_allow_html=True)
            
            if total_files > 0:
                st.markdown("**Category Breakdown:**")
                for category, count in category_counts.items():
                    if count > 0:
                        percentage = (count / total_files * 100)
                        st.markdown(f"""
                        <div style='
                            background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
                            border-left: 4px solid #667eea;
                            padding: 0.75rem;
                            margin: 0.5rem 0;
                            border-radius: 0 8px 8px 0;
                        '>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong style="color: #2d3748;">{category}</strong>
                                <span style="color: #4a5568;">{count:,}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #718096; margin-top: 0.25rem;">
                                {percentage:.1f}% of total files
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Duplicate detection
            st.markdown("---")
            st.markdown("#### 🔍 Duplicate Detection")
            with st.spinner("Scanning for duplicates..."):
                duplicates = self.organizer.find_duplicates(folder_path, include_hidden)
            
            if duplicates:
                total_duplicates = sum(len(files) - 1 for files in duplicates.values())
                st.markdown(f"""
                <div class="warning-alert" style="padding: 0.75rem; margin: 0.5rem 0;">
                    <strong>⚠️ Duplicates Found</strong><br>
                    <small>{total_duplicates} duplicate files in {len(duplicates)} groups</small>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📋 View Duplicate Details"):
                    for i, (hash_val, file_list) in enumerate(duplicates.items()):
                        if i < 3:  # Show only first 3 groups to avoid clutter
                            st.markdown(f"**Group {i+1} ({len(file_list)} files):**")
                            for file_path in file_list:
                                filename = os.path.basename(file_path)
                                st.markdown(f"<div class='file-item'>{filename}</div>", unsafe_allow_html=True)
                            if i < len(duplicates) - 1:
                                st.markdown("---")
                        elif i == 3:
                            st.info(f"... and {len(duplicates) - 3} more duplicate groups")
                            break
            else:
                st.markdown("""
                <div class="success-alert" style="padding: 0.75rem; margin: 0.5rem 0;">
                    ✅ <strong>No Duplicates Found</strong>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown(f"""
            <div class="error-alert" style="padding: 0.75rem; margin: 0.5rem 0;">
                ❌ <strong>Analysis Error:</strong><br>
                <small>{str(e)}</small>
            </div>
            """, unsafe_allow_html=True)
    
    def render_main_content(self, folder_path: str):
        """Render the enhanced main content area."""
        # Create main layout columns
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if folder_path:
                if os.path.exists(folder_path):
                    st.markdown(f"""
                    <div class="success-alert slide-in">
                        <h3 style="margin: 0; color: #2d3748;">✅ Directory Validated</h3>
                        <p style="margin: 0.5rem 0; font-family: monospace; background: rgba(0,0,0,0.05); 
                           padding: 0.5rem; border-radius: 4px;">{folder_path}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    self._render_directory_preview(folder_path)
                elif folder_path.strip():
                    st.markdown("""
                    <div class="error-alert">
                        <h3 style="margin: 0; color: #2d3748;">❌ Directory Not Found</h3>
                        <p style="margin: 0.5rem 0;">Please verify the path exists and you have access permissions.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-alert">
                    <h3 style="margin: 0; color: #2d3748;">👈 Getting Started</h3>
                    <p style="margin: 0.5rem 0;">Enter a directory path in the control panel to begin file organization.</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            return self._render_control_panel(folder_path)
    
    def _render_directory_preview(self, folder_path: str):
        """Render enhanced directory structure preview."""
        with st.expander("📋 Directory Structure Preview", expanded=False):
            try:
                items = sorted(os.listdir(folder_path))
                total_items = len(items)
                preview_items = items[:20]  # Show first 20 items
                
                if preview_items:
                    # Create responsive columns
                    col1, col2 = st.columns(2)
                    
                    for i, item in enumerate(preview_items):
                        item_path = os.path.join(folder_path, item)
                        target_col = col1 if i % 2 == 0 else col2
                        
                        with target_col:
                            if os.path.isdir(item_path):
                                st.markdown(f"""
                                <div class="file-item">
                                    <span style="color: #ed8936;">📁</span> <strong>{item}/</strong>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                try:
                                    file_size = os.path.getsize(item_path)
                                    size_str = self.utils.format_file_size(file_size)
                                    file_icon = self._get_file_icon(item)
                                    
                                    st.markdown(f"""
                                    <div class="file-item">
                                        <span>{file_icon}</span> {item}
                                        <br><small style="color: #718096;">{size_str}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                                except Exception:
                                    file_icon = self._get_file_icon(item)
                                    st.markdown(f"""
                                    <div class="file-item">
                                        <span>{file_icon}</span> {item}
                                        <br><small style="color: #718096;">Size unknown</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                    
                    if total_items > 20:
                        st.markdown(f"""
                        <div class="info-alert" style="text-align: center; padding: 0.75rem; margin-top: 1rem;">
                            <strong>... and {total_items - 20} more items</strong>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="info-alert" style="text-align: center;">
                        📭 <strong>Directory is empty</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except PermissionError:
                st.markdown("""
                <div class="error-alert">
                    🚫 <strong>Access Denied:</strong> Insufficient permissions to read this directory.
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-alert">
                    ⚠️ <strong>Error:</strong> {str(e)}
                </div>
                """, unsafe_allow_html=True)
    
    def _get_file_icon(self, filename: str) -> str:
        """Get appropriate icon for file type."""
        ext = os.path.splitext(filename)[1].lower()
        
        icon_map = {
            # Documents
            '.pdf': '📄', '.doc': '📄', '.docx': '📄', '.txt': '📄',
            '.rtf': '📄', '.odt': '📄',
            
            # Spreadsheets
            '.xls': '📊', '.xlsx': '📊', '.csv': '📊', '.ods': '📊',
            
            # Presentations
            '.ppt': '📽️', '.pptx': '📽️', '.odp': '📽️',
            
            # Images
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
            '.bmp': '🖼️', '.svg': '🖼️', '.tiff': '🖼️', '.webp': '🖼️',
            
            # Videos
            '.mp4': '🎬', '.avi': '🎬', '.mov': '🎬', '.wmv': '🎬',
            '.flv': '🎬', '.mkv': '🎬', '.webm': '🎬',
            
            # Audio
            '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵', '.aac': '🎵',
            '.ogg': '🎵', '.wma': '🎵',
            
            # Archives
            '.zip': '📦', '.rar': '📦', '.7z': '📦', '.tar': '📦',
            '.gz': '📦', '.bz2': '📦',
            
            # Code
            '.py': '🐍', '.js': '💛', '.html': '🌐', '.css': '🎨',
            '.java': '☕', '.cpp': '⚙️', '.c': '⚙️', '.php': '🐘',
            '.rb': '💎', '.go': '🐹', '.rs': '🦀',
            
            # Executables
            '.exe': '⚙️', '.msi': '⚙️', '.deb': '📦', '.rpm': '📦',
        }
        
        return icon_map.get(ext, '📄')
    
    def _render_control_panel(self, folder_path: str) -> Tuple[bool, bool]:
        """Render the enhanced control panel."""
        st.markdown("### 🚀 Action Center")
        
        # Status indicator
        if folder_path and os.path.exists(folder_path):
            st.markdown("""
            <div class="status-card status-ready">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🟢</div>
                <h3 style="margin: 0; font-size: 1.2rem;">SYSTEM READY</h3>
                <p style="margin: 0.5rem 0; opacity: 0.9;">All systems operational</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-card status-standby">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🟡</div>
                <h3 style="margin: 0; font-size: 1.2rem;">STANDBY MODE</h3>
                <p style="margin: 0.5rem 0; opacity: 0.9;">Awaiting directory selection</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Action buttons with enhanced styling
        organize_button = st.button(
            "🗂️ Execute Organization",
            type="primary",
            disabled=not (folder_path and os.path.exists(folder_path)),
            use_container_width=True,
            help="Begin intelligent file organization process"
        )
        
        st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
        
        undo_button = st.button(
            "↩️ Rollback Last Operation",
            use_container_width=True,
            help="Revert the most recent organization changes"
        )
        
        # Quick actions
        if folder_path and os.path.exists(folder_path):
            st.markdown("---")
            st.markdown("#### ⚡ Quick Actions")
            
            col1, col2 = st.columns(2)
            with col1:
                analyze_btn = st.button("📊 Analyze", use_container_width=True, key="quick_analyze")
            with col2:
                verify_btn = st.button("🔍 Verify", use_container_width=True, key="quick_verify")
            
            return organize_button, undo_button, analyze_btn, verify_btn
        
        return organize_button, undo_button, False, False
    
    # def handle_organization(self, folder_path: str, flatten_structure: bool, show_hidden: bool):
    #     """Handle the enhanced organization process."""
    #     if not folder_path or not os.path.exists(folder_path):
    #         st.markdown("""
    #         <div class="error-alert">
    #             <h3 style="margin: 0;">🚫 Operation Failed</h3>
    #             <p style="margin: 0.5rem 0;">Please select a valid directory first.</p>
    #         </div>
    #         """, unsafe_allow_html=True)
    #         return
        
    #     st.markdown("## 🔄 Organization Process")
        
    #     # Progress tracking
    #     progress_container = st.container()
    #     with progress_container:
    #         progress_bar = st.progress(0)
    #         status_container = st.empty()
            
    #     start_time = time.time()
        
    #     def update_progress(progress, current_file=""):
    #         progress_bar.progress(progress)
    #         elapsed = time.time() - start_time
    #         estimated_total = elapsed / progress if progress > 0 else 0
    #         remaining = max(0, estimated_total - elapsed)
            
    #         status_container.markdown(f"""
    #         <div class="metric-card" style="text-align: center;">
    #             <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
    #                 <div>
    #                     <strong style="color: #667eea;">Progress</strong><br>
    #                     <span style="font-size: 1.5rem; color: #2d3748;">{int(progress * 100)}%</span>
    #                 </div>
    #                 <div>
    #                     <strong style="color: #667eea;">Elapsed</strong><br>
    #                     <span style="font-size: 1.5rem; color: #2d3748;">{elapsed:.1f}s</span>
    #                 </div>
    #                 <div>
    #                     <strong style="color: #667eea;">Remaining</strong><br>
    #                     <span style="font-size: 1.5rem; color: #2d3748;">{remaining:.1f}s</span>
    #                 </div>
    #             </div>
    #             {f'<p style="color: #718096; margin: 0;"><strong>Processing:</strong> {current_file}</p>' if current_file else ''}
    #         </div>
    #         """, unsafe_allow_html=True)
        
    #     # Execute organization
    #     try:
    #         success, message = self.organizer.organize_files(
    #         folder_path,
    #         flatten_structure,
    #         show_hidden,
    #         progress_callback=update_progress  # support current_file if implemented
    #     )
    #     except Exception as e:
    #         st.markdown(f"""
    #     <div class="error-box">
    #         <h3 style="margin: 0;">❌ Unexpected Error</h3>
    #         <p>{str(e)}</p>
    #     </div>
    #     """, unsafe_allow_html=True)
    #     return

    #     total_time = time.time() - start_time
    #     progress_bar.progress(1.0)
    
    def handle_organization(self, folder_path: str, flatten_structure: bool, show_hidden: bool):
        """Handle the enhanced organization process."""
        if not folder_path or not os.path.exists(folder_path):
            st.markdown("""
            <div class="error-alert">
                <h3 style="margin: 0;">🚫 Operation Failed</h3>
                <p style="margin: 0.5rem 0;">Please select a valid directory first.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        st.markdown("## 🔄 Organization Process")

        # Progress tracking
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_container = st.empty()

        start_time = time.time()

        def update_progress(progress, current_file=""):
            progress_bar.progress(progress)
            elapsed = time.time() - start_time
            estimated_total = elapsed / progress if progress > 0 else 0
            remaining = max(0, estimated_total - elapsed)

            status_container.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <div>
                        <strong style="color: #667eea;">Progress</strong><br>
                        <span style="font-size: 1.5rem; color: #2d3748;">{int(progress * 100)}%</span>
                    </div>
                    <div>
                        <strong style="color: #667eea;">Elapsed</strong><br>
                        <span style="font-size: 1.5rem; color: #2d3748;">{elapsed:.1f}s</span>
                    </div>
                    <div>
                        <strong style="color: #667eea;">Remaining</strong><br>
                        <span style="font-size: 1.5rem; color: #2d3748;">{remaining:.1f}s</span>
                    </div>
                </div>
                {f'<p style="color: #718096; margin: 0;"><strong>Processing:</strong> {current_file}</p>' if current_file else ''}
            </div>
            """, unsafe_allow_html=True)

        # Execute organization
        try:
            success, message = self.organizer.organize_files(
                folder_path,
                flatten_structure,
                show_hidden,
                progress_callback=update_progress
            )
            
            total_time = time.time() - start_time
            progress_bar.progress(1.0)
            
            # Show results
            if success:
                st.markdown(f"""
                <div class="success-alert slide-in">
                    <h3 style="margin: 0; color: #2d3748;">✅ Organization Complete!</h3>
                    <p style="margin: 0.5rem 0;">{message}</p>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.1);">
                        <strong>📊 Process Summary:</strong><br>
                        <small style="color: #4a5568;">
                            • Total time: {total_time:.2f} seconds<br>
                            • Directory: {folder_path}<br>
                            • Flattened structure: {'Yes' if flatten_structure else 'No'}<br>
                            • Hidden files included: {'Yes' if show_hidden else 'No'}
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show post-organization stats
                self._show_organization_summary(folder_path)
                
            else:
                st.markdown(f"""
                <div class="error-alert">
                    <h3 style="margin: 0; color: #2d3748;">❌ Organization Failed</h3>
                    <p style="margin: 0.5rem 0;">{message}</p>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.1);">
                        <small style="color: #4a5568;">
                            Time elapsed: {total_time:.2f} seconds<br>
                            Check file permissions and available disk space.
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            total_time = time.time() - start_time
            st.markdown(f"""
            <div class="error-alert">
                <h3 style="margin: 0; color: #2d3748;">❌ Unexpected Error</h3>
                <p style="margin: 0.5rem 0;">An error occurred during organization: {str(e)}</p>
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.1);">
                    <small style="color: #4a5568;">
                        Time elapsed: {total_time:.2f} seconds<br>
                        Please check the error details and try again.
                    </small>
                </div>
            </div>
            """, unsafe_allow_html=True)

    def _show_organization_summary(self, folder_path: str):
        """Show detailed summary after organization."""
        st.markdown("### 📈 Organization Summary")
        
        try:
            # Get updated file counts
            category_counts = self.organizer.count_files_by_category(folder_path, include_hidden=False)
            total_files = sum(category_counts.values())
            
            # Create summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📁 Total Files",
                    value=f"{total_files:,}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="🗂️ Categories",
                    value=len([c for c, count in category_counts.items() if count > 0]),
                    delta=None
                )
            
            with col3:
                largest_category = max(category_counts.items(), key=lambda x: x[1]) if category_counts else ("None", 0)
                st.metric(
                    label="📊 Largest Category",
                    value=largest_category[0],
                    delta=f"{largest_category[1]} files"
                )
            
            with col4:
                # Calculate organization efficiency (files organized vs total)
                organized_files = sum(count for cat, count in category_counts.items() if cat != "Other")
                efficiency = (organized_files / total_files * 100) if total_files > 0 else 0
                st.metric(
                    label="🎯 Organization Rate",
                    value=f"{efficiency:.1f}%",
                    delta=None
                )
            
            # Show category breakdown chart
            if category_counts:
                st.markdown("#### 📊 File Distribution After Organization")
                
                # Filter out empty categories
                filtered_counts = {cat: count for cat, count in category_counts.items() if count > 0}
                
                if filtered_counts:
                    chart_df = pd.DataFrame([
                        {'Category': cat, 'Count': count}
                        for cat, count in filtered_counts.items()
                    ])
                    
                    # Create horizontal bar chart
                    fig = px.bar(
                        chart_df,
                        x='Count',
                        y='Category',
                        orientation='h',
                        title='Files by Category',
                        color='Count',
                        color_continuous_scale='Viridis'
                    )
                    
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.markdown(f"""
            <div class="warning-alert">
                <h4 style="margin: 0;">⚠️ Summary Generation Error</h4>
                <p style="margin: 0.5rem 0;">Could not generate organization summary: {str(e)}</p>
            </div>
            """, unsafe_allow_html=True)

    def handle_undo(self):
        """Handle the enhanced undo operation."""
        st.markdown("## ↩️ Rollback Operation")
        
        try:
            success, message = self.organizer.undo_last_organization()
            
            if success:
                st.markdown(f"""
                <div class="success-alert slide-in">
                    <h3 style="margin: 0; color: #2d3748;">✅ Rollback Successful</h3>
                    <p style="margin: 0.5rem 0;">{message}</p>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.1);">
                        <small style="color: #4a5568;">
                            All files have been restored to their original locations.
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="error-alert">
                    <h3 style="margin: 0; color: #2d3748;">❌ Rollback Failed</h3>
                    <p style="margin: 0.5rem 0;">{message}</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown(f"""
            <div class="error-alert">
                <h3 style="margin: 0; color: #2d3748;">❌ Rollback Error</h3>
                <p style="margin: 0.5rem 0;">An error occurred during rollback: {str(e)}</p>
            </div>
            """, unsafe_allow_html=True)

    def render_footer(self):
        """Render the professional footer."""
        st.markdown("""
        <div class="footer">
            <h3 style="margin: 0 0 1rem 0; color: #e2e8f0;">Enterprise File Organizer</h3>
            <p style="margin: 0; opacity: 0.8;">
                Advanced file management solution with intelligent categorization and comprehensive analytics.
            </p>
            <div style="margin: 1rem 0; padding: 1rem 0; border-top: 1px solid rgba(226, 232, 240, 0.2);">
                <small style="opacity: 0.7;">
                    Built with Streamlit • Powered by Python • 
                    <span style="color: #f687b3;">Made with ❤️</span>
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def render(self):
        """Main application entry point with enhanced flow control."""
        try:
            # Render header
            self.render_header()
            
            # Get configuration from sidebar
            folder_path, flatten_structure, show_hidden = self.render_sidebar()
            
            # Render main content and get button states
            button_results = self.render_main_content(folder_path)
            
            # Handle different button combinations
            if len(button_results) == 4:
                organize_btn, undo_btn, analyze_btn, verify_btn = button_results
            else:
                organize_btn, undo_btn = button_results
                analyze_btn = verify_btn = False
            
            # Handle button actions
            if organize_btn:
                self.handle_organization(folder_path, flatten_structure, show_hidden)
                st.rerun()  # Refresh the app after organization
            
            if undo_btn:
                self.handle_undo()
                st.rerun()  # Refresh the app after undo
            
            if analyze_btn and folder_path and os.path.exists(folder_path):
                self.render_analysis(folder_path)
            
            if verify_btn and folder_path and os.path.exists(folder_path):
                self._perform_directory_verification(folder_path)
            
            # Render footer
            self.render_footer()
            
        except Exception as e:
            st.markdown(f"""
            <div class="error-alert">
                <h3 style="margin: 0; color: #2d3748;">🚨 Application Error</h3>
                <p style="margin: 0.5rem 0;">A critical error occurred: {str(e)}</p>
                <details style="margin-top: 1rem;">
                    <summary style="cursor: pointer; color: #4a5568;">Click for technical details</summary>
                    <pre style="background: rgba(0,0,0,0.05); padding: 1rem; border-radius: 4px; margin-top: 0.5rem; font-size: 0.8rem; overflow-x: auto;">
{str(e)}
                    </pre>
                </details>
            </div>
            """, unsafe_allow_html=True)

    def _perform_directory_verification(self, folder_path: str):
        """Perform comprehensive directory verification."""
        st.markdown("### 🔍 Directory Verification")
        
        with st.spinner("Performing comprehensive directory verification..."):
            verification_results = {}
            
            try:
                # Check accessibility
                verification_results['accessibility'] = os.access(folder_path, os.R_OK | os.W_OK)
                
                # Check for broken symlinks
                broken_links = []
                for root, dirs, files in os.walk(folder_path):
                    for item in dirs + files:
                        item_path = os.path.join(root, item)
                        if os.path.islink(item_path) and not os.path.exists(item_path):
                            broken_links.append(item_path)
                
                verification_results['broken_links'] = broken_links
                
                # Check for empty directories
                empty_dirs = []
                for root, dirs, files in os.walk(folder_path):
                    if not dirs and not files and root != folder_path:
                        empty_dirs.append(root)
                
                verification_results['empty_directories'] = empty_dirs
                
                # Check file permissions
                permission_issues = []
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            if not os.access(file_path, os.R_OK):
                                permission_issues.append(f"Read access denied: {file_path}")
                        except Exception as e:
                            permission_issues.append(f"Permission check failed: {file_path} - {str(e)}")
                
                verification_results['permission_issues'] = permission_issues[:10]  # Limit to first 10
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-alert">
                    <h4 style="margin: 0;">❌ Verification Failed</h4>
                    <p style="margin: 0.5rem 0;">Error during verification: {str(e)}</p>
                </div>
                """, unsafe_allow_html=True)
                return
        
        # Display verification results
        col1, col2 = st.columns(2)
        
        with col1:
            # Accessibility check
            if verification_results['accessibility']:
                st.markdown("""
                <div class="success-alert">
                    <h4 style="margin: 0;">✅ Directory Access</h4>
                    <p style="margin: 0.5rem 0;">Read and write permissions verified</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-alert">
                    <h4 style="margin: 0;">❌ Access Issues</h4>
                    <p style="margin: 0.5rem 0;">Insufficient permissions detected</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Broken symlinks
            broken_count = len(verification_results['broken_links'])
            if broken_count == 0:
                st.markdown("""
                <div class="success-alert">
                    <h4 style="margin: 0;">✅ Symlink Integrity</h4>
                    <p style="margin: 0.5rem 0;">No broken symbolic links found</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-alert">
                    <h4 style="margin: 0;">⚠️ Broken Symlinks</h4>
                    <p style="margin: 0.5rem 0;">{broken_count} broken symbolic links detected</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Empty directories
            empty_count = len(verification_results['empty_directories'])
            if empty_count == 0:
                st.markdown("""
                <div class="success-alert">
                    <h4 style="margin: 0;">✅ Directory Structure</h4>
                    <p style="margin: 0.5rem 0;">No empty directories found</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="info-alert">
                    <h4 style="margin: 0;">ℹ️ Empty Directories</h4>
                    <p style="margin: 0.5rem 0;">{empty_count} empty directories found</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Permission issues
            perm_count = len(verification_results['permission_issues'])
            if perm_count == 0:
                st.markdown("""
                <div class="success-alert">
                    <h4 style="margin: 0;">✅ File Permissions</h4>
                    <p style="margin: 0.5rem 0;">All files accessible</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-alert">
                    <h4 style="margin: 0;">⚠️ Permission Issues</h4>
                    <p style="margin: 0.5rem 0;">{perm_count}+ files with access issues</p>
                </div>
                """, unsafe_allow_html=True)


# Main application entry point
if __name__ == "__main__":
    app = StreamlitUI()
    app.render()