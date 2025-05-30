class FileOrganizerConfig:
    """Configuration constants for the file organizer."""
    LOG_FILE = "logger_json//file_organizer_log.json"
    DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"
    HASH_BLOCK_SIZE = 65536
    
    EXTENSIONS_MAPPING = {
        "Images": ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'),
        "Documents": ('.pdf', '.doc', '.docx', '.csv', '.xls', '.xlsx', '.pptx', '.txt', '.rtf'),
        "Audio": ('.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'),
        "Videos": ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'),
        "Archives": ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'),
        "Code": ('.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.sh'),
        "Executables": ('.exe', '.msi', '.dmg', '.pkg', '.deb'),
        "Others": ()  # Default category
    }