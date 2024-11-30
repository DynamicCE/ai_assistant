import sqlite3
from datetime import datetime
from typing import Optional, List, Dict
import json

class Database:
    def __init__(self):
        self.db_path = "resources/assistant.db"
        self._create_tables()
    
    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Konuşma geçmişi tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_input TEXT,
                    assistant_response TEXT,
                    command_type TEXT,
                    success BOOLEAN
                )
            """)
            
            # Kullanıcı ayarları tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Komut istatistikleri tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS command_stats (
                    command TEXT PRIMARY KEY,
                    usage_count INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0,
                    last_used DATETIME
                )
            """)
            
            conn.commit()
    
    def save_conversation(self, user_input: str, response: str, 
                         command_type: str, success: bool) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversations 
                (user_input, assistant_response, command_type, success)
                VALUES (?, ?, ?, ?)
            """, (user_input, response, command_type, success))
            
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def update_setting(self, key: str, value: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, value))
    
    def get_setting(self, key: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def update_command_stats(self, command: str, success: bool) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO command_stats (command, usage_count, success_rate, last_used)
                VALUES (?, 1, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(command) DO UPDATE SET
                    usage_count = usage_count + 1,
                    success_rate = (
                        (success_rate * usage_count + ?) / (usage_count + 1)
                    ),
                    last_used = CURRENT_TIMESTAMP
            """, (command, 1 if success else 0, 1 if success else 0)) 