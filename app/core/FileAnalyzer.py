import os
from datetime import datetime
from typing import Dict, List, Tuple
from app.core.FileUtils import FileUtils
from app.config.FileOrganiserConfig import FileOrganizerConfig

class FileAnalyzer:
    """Analyzes file organization and generates reports."""
    
    def __init__(self):
        self.file_utils = FileUtils()
    
    def analyze_storage_usage(self, directory: str) -> Dict[str, float]:
        """Analyze storage usage by category."""
        usage_by_category = {category: 0 for category in FileOrganizerConfig.EXTENSIONS_MAPPING.keys()}
        
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if not self.file_utils.is_hidden_file(filename):
                    category = self.file_utils.get_file_category(filename)
                    file_path = os.path.join(dirpath, filename)
                    try:
                        usage_by_category[category] += os.path.getsize(file_path)
                    except OSError:
                        continue
        
        return {cat: self.file_utils.format_file_size(size) for cat, size in usage_by_category.items()}
    
    def get_file_distribution(self, directory: str) -> Dict[str, int]:
        """Get file type distribution statistics."""
        distribution = {category: 0 for category in FileOrganizerConfig.EXTENSIONS_MAPPING.keys()}
        
        for _, _, filenames in os.walk(directory):
            for filename in filenames:
                if not self.file_utils.is_hidden_file(filename):
                    category = self.file_utils.get_file_category(filename)
                    distribution[category] += 1
        
        return distribution
    
    def get_age_distribution(self, directory: str) -> Dict[str, List[str]]:
        """Analyze files by age (last modified date)."""
        age_ranges = {
            'Last 24 hours': [],
            'Last week': [],
            'Last month': [],
            'Last year': [],
            'Older': []
        }
        
        now = datetime.now()
        
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if self.file_utils.is_hidden_file(filename):
                    continue
                    
                file_path = os.path.join(dirpath, filename)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    age = now - mtime
                    
                    if age.days < 1:
                        age_ranges['Last 24 hours'].append(filename)
                    elif age.days < 7:
                        age_ranges['Last week'].append(filename)
                    elif age.days < 30:
                        age_ranges['Last month'].append(filename)
                    elif age.days < 365:
                        age_ranges['Last year'].append(filename)
                    else:
                        age_ranges['Older'].append(filename)
                except OSError:
                    continue
        
        return age_ranges
    
    def generate_disk_space_report(self, directory: str) -> Dict[str, str]:
        """Generate detailed disk space usage report."""
        total_size = 0
        largest_files = []
        
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if self.file_utils.is_hidden_file(filename):
                    continue
                    
                file_path = os.path.join(dirpath, filename)
                try:
                    size = os.path.getsize(file_path)
                    total_size += size
                    largest_files.append((file_path, size))
                except OSError:
                    continue
        
        largest_files.sort(key=lambda x: x[1], reverse=True)
        top_files = [(f, self.file_utils.format_file_size(s)) for f, s in largest_files[:10]]
        
        return {
            'total_space': self.file_utils.format_file_size(total_size),
            'largest_files': dict(top_files)
        }