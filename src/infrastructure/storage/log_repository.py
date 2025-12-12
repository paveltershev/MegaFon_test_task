import sqlite3
from datetime import datetime
from src.domain.interfaces import LogRepository

class SQLiteLogRepository(LogRepository):
    def __init__(self, db_path: str = "logs.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                error TEXT
            )
        """)
        conn.commit()
        conn.close()

    def log_request(self, city: str, success: bool, error: str = ""):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO requests (city, timestamp, success, error) VALUES (?, ?, ?, ?)",
            (city, datetime.now().isoformat(), success, error)
        )
        conn.commit()
        conn.close()