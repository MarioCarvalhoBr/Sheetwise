"""
Data models for Sheetwise application
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

class DatabaseManager:
    """SQLite database connection manager"""
    
    def __init__(self, db_path: str = "database/sheetwise.db"):
        self.db_path = db_path
        self._ensure_database_directory()
        self._create_tables()
    
    def _ensure_database_directory(self):
        """Ensure database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _create_tables(self):
        """Create necessary database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Executions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    protocol TEXT NOT NULL,
                    department TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    source_folder_path TEXT NOT NULL,
                    result_file_path TEXT NOT NULL,
                    execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'completed',
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Configurations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configurations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    theme TEXT DEFAULT 'cosmo',
                    language TEXT DEFAULT 'en',
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(user_id)
                )
            ''')
            
            conn.commit()
    
    def get_connection(self):
        """Return database connection"""
        return sqlite3.connect(self.db_path)


class User:
    """User model"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_user(self, username: str, email: str) -> int:
        """Create a new user"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (username, email)
            )
            return cursor.lastrowid
    
    def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, registration_date FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'registration_date': row[3]
                }
        return None
    
    def list_users(self) -> List[Dict[str, Any]]:
        """List all users"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, registration_date FROM users ORDER BY username"
            )
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'registration_date': row[3]
                }
                for row in rows
            ]


class Execution:
    """Execution model"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_execution(self, user_id: int, protocol: str, department: str, 
                        filename: str, source_folder_path: str,
                        result_file_path: str, notes: str = "") -> int:
        """Create a new execution"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO executions 
                (user_id, protocol, department, filename, source_folder_path,
                 result_file_path, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, protocol, department, filename, source_folder_path,
                  result_file_path, notes))
            return cursor.lastrowid
    
    def list_executions(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """List executions, optionally filtered by user"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT e.id, e.protocol, e.department, e.filename,
                           e.source_folder_path, e.result_file_path,
                           e.execution_date, e.status, e.notes,
                           u.username as user_username
                    FROM executions e
                    JOIN users u ON e.user_id = u.id
                    WHERE e.user_id = ?
                    ORDER BY e.execution_date DESC
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT e.id, e.protocol, e.department, e.filename,
                           e.source_folder_path, e.result_file_path,
                           e.execution_date, e.status, e.notes,
                           u.username as user_username
                    FROM executions e
                    JOIN users u ON e.user_id = u.id
                    ORDER BY e.execution_date DESC
                ''')
            
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'protocol': row[1],
                    'department': row[2],
                    'filename': row[3],
                    'source_folder_path': row[4],
                    'result_file_path': row[5],
                    'execution_date': row[6],
                    'status': row[7],
                    'notes': row[8],
                    'user_username': row[9]
                }
                for row in rows
            ]
    
    def find_execution_by_id(self, execution_id: int) -> Optional[Dict[str, Any]]:
        """Find execution by ID"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.id, e.protocol, e.department, e.filename,
                       e.source_folder_path, e.result_file_path,
                       e.execution_date, e.status, e.notes,
                       u.username as user_username, e.user_id
                FROM executions e
                JOIN users u ON e.user_id = u.id
                WHERE e.id = ?
            ''', (execution_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'protocol': row[1],
                    'department': row[2],
                    'filename': row[3],
                    'source_folder_path': row[4],
                    'result_file_path': row[5],
                    'execution_date': row[6],
                    'status': row[7],
                    'notes': row[8],
                    'user_username': row[9],
                    'user_id': row[10]
                }
        return None
    
    def delete_execution(self, execution_id: int) -> bool:
        """Delete an execution"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM executions WHERE id = ?", (execution_id,))
            return cursor.rowcount > 0
    
    def update_execution_status(self, execution_id: int, status: str, 
                               notes: str = "") -> bool:
        """Update execution status"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE executions 
                SET status = ?, notes = ?
                WHERE id = ?
            ''', (status, notes, execution_id))
            return cursor.rowcount > 0


class ConfigurationManager:
    """User configuration manager"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_configuration(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user configuration"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT theme, language, last_updated
                FROM configurations 
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'theme': row[0],
                    'language': row[1],
                    'last_updated': row[2]
                }
        return None
    
    def get_configuration_or_create(self, user_id: int) -> Dict[str, Any]:
        """Get configuration or create default if doesn't exist"""
        config = self.get_configuration(user_id)
        if config is None:
            # Create default configuration
            self.save_configuration(user_id, 'cosmo', 'en')
            config = {
                'theme': 'cosmo',
                'language': 'en',
                'last_updated': datetime.now().isoformat()
            }
        return config
    
    def save_configuration(self, user_id: int, theme: str, language: str) -> bool:
        """Save user configuration"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if configuration already exists
            existing = self.get_configuration(user_id)
            
            if existing:
                # Update existing configuration
                cursor.execute('''
                    UPDATE configurations 
                    SET theme = ?, language = ?, 
                        last_updated = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (theme, language, user_id))
            else:
                # Insert new configuration
                cursor.execute('''
                    INSERT INTO configurations 
                    (user_id, theme, language)
                    VALUES (?, ?, ?)
                ''', (user_id, theme, language))
            
            return cursor.rowcount > 0
    
    def update_theme(self, user_id: int, theme: str) -> bool:
        """Update theme only"""
        config = self.get_configuration_or_create(user_id)
        return self.save_configuration(user_id, theme, config['language'])
    
    def update_language(self, user_id: int, language: str) -> bool:
        """Update language only"""
        config = self.get_configuration_or_create(user_id)
        return self.save_configuration(user_id, config['theme'], language)
    
    def get_available_themes(self) -> Dict[str, str]:
        """Return available ttkbootstrap themes"""
        return {
            # Light themes
            'cosmo': 'Cosmo (Light)',
            'flatly': 'Flatly (Light)',
            'journal': 'Journal (Light)',
            'litera': 'Litera (Light)',
            'lumen': 'Lumen (Light)',
            'minty': 'Minty (Light)',
            'pulse': 'Pulse (Light)',
            'sandstone': 'Sandstone (Light)',
            'united': 'United (Light)',
            'yeti': 'Yeti (Light)',
            'morph': 'Morph (Light)',
            'simplex': 'Simplex (Light)',
            'cerculean': 'Cerculean (Light)',
            
            # Dark themes
            'solar': 'Solar (Dark)',
            'superhero': 'Superhero (Dark)',
            'darkly': 'Darkly (Dark)',
            'cyborg': 'Cyborg (Dark)',
            'vapor': 'Vapor (Dark)'
        }
    
    def get_last_user_theme(self) -> str:
        """Get the theme of the last user who logged in (based on last_updated)"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT theme FROM configurations 
                ORDER BY last_updated DESC 
                LIMIT 1
            ''')
            result = cursor.fetchone()
            return result[0] if result else 'cosmo'