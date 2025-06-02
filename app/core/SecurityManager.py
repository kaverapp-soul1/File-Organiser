import os
import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from pathlib import Path

class SecurityManager:
    """Manages security features for the file organizer."""
    
    def __init__(self, config_path: str = 'security_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_encryption()
        self._setup_logging()
    
    def _setup_encryption(self):
        """Initialize encryption key."""
        if not self.config.get('encryption_key'):
            key = Fernet.generate_key()
            self.config['encryption_key'] = key.decode()
            self._save_config()
        self.fernet = Fernet(self.config['encryption_key'].encode())
    
    def _setup_logging(self):
        """Setup security logging."""
        logging.basicConfig(
            filename='security.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def _load_config(self) -> Dict:
        """Load security configuration."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_config(self):
        """Save security configuration."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def encrypt_file(self, file_path: str) -> bool:
        """Encrypt a file."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted_data = self.fernet.encrypt(data)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            logging.info(f'File encrypted: {file_path}')
            return True
        except Exception as e:
            logging.error(f'Encryption failed for {file_path}: {str(e)}')
            return False
    
    def decrypt_file(self, file_path: str) -> bool:
        """Decrypt a file."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            decrypted_data = self.fernet.decrypt(data)
            with open(file_path, 'wb') as f:
                f.write(decrypted_data)
            logging.info(f'File decrypted: {file_path}')
            return True
        except Exception as e:
            logging.error(f'Decryption failed for {file_path}: {str(e)}')
            return False
    
    def verify_file_integrity(self, file_path: str, stored_hash: Optional[str] = None) -> bool:
        """Verify file integrity using SHA-256."""
        try:
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            current_hash = sha256.hexdigest()
            
            if stored_hash:
                return current_hash == stored_hash
            
            return current_hash
        except Exception as e:
            logging.error(f'Integrity check failed for {file_path}: {str(e)}')
            return False
    
    def log_access(self, file_path: str, action: str, user: str = 'system'):
        """Log file access."""
        logging.info(f'Access: {user} - {action} - {file_path}')
    
    def set_file_password(self, file_path: str, password: str):
        """Set password protection for a file."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.config.setdefault('protected_files', {})[file_path] = password_hash
        self._save_config()
        logging.info(f'Password protection set for: {file_path}')
    
    def verify_file_password(self, file_path: str, password: str) -> bool:
        """Verify password for a protected file."""
        protected_files = self.config.get('protected_files', {})
        if file_path not in protected_files:
            return True
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return protected_files[file_path] == password_hash