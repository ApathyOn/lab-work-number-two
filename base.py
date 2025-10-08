# base.py
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
import functools

def init_db():
    conn = sqlite3.connect("museum.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            title TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS views (
            item_id INTEGER NOT NULL,
            visitor_id TEXT NOT NULL,
            watch_time REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_action(message):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

class Viewable(ABC):
    def __init__(self, title):
        self.title = title
        conn = sqlite3.connect("museum.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO items (type, title) VALUES (?, ?)",
                    (self.get_type_name(), self.title))
        self.db_id = cur.lastrowid
        conn.commit()
        conn.close()

    @abstractmethod
    def get_type_name(self):
        pass

    @log_action("Просмотр зафиксирован")
    def add_view(self, visitor_id, watch_time_sec):
        if watch_time_sec < 0:
            raise ValueError("Время просмотра не может быть отрицательным")
        conn = sqlite3.connect("museum.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO views (item_id, visitor_id, watch_time) VALUES (?, ?, ?)",
                    (self.db_id, visitor_id, watch_time_sec))
        conn.commit()
        conn.close()

    def get_stats(self):
        conn = sqlite3.connect("museum.db")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), AVG(watch_time) FROM views WHERE item_id = ?", (self.db_id,))
        count, avg = cur.fetchone()
        conn.close()
        return count or 0, avg or 0.0

    def __str__(self):
        views, avg = self.get_stats()
        return f"{self.get_type_name()} '{self.title}': {views} просмотров, ср. время: {avg:.1f} сек"

    def __repr__(self):
        return f"{self.__class__.__name__}(title='{self.title}')"