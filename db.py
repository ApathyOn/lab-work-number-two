# db.py
import sqlite3

# Имя БД по умолчанию (для основного приложения)
DEFAULT_DB_PATH = "museum_summary.db"


def get_connection(db_path=None):
    """Вспомогательная функция для получения соединения."""
    return sqlite3.connect(db_path or DEFAULT_DB_PATH)


def init_db(db_path=None):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS totals (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            count INTEGER NOT NULL DEFAULT 0
        )
    ''')
    cur.execute("INSERT OR IGNORE INTO totals (id, name, count) VALUES (1, 'Экспонаты', 0)")
    cur.execute("INSERT OR IGNORE INTO totals (id, name, count) VALUES (2, 'Статьи', 0)")
    conn.commit()
    conn.close()


def save_totals(total_exhibits, total_articles, db_path=None):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE totals SET count = ? WHERE name = 'Экспонаты'", (total_exhibits,))
    cur.execute("UPDATE totals SET count = ? WHERE name = 'Статьи'", (total_articles,))
    conn.commit()
    conn.close()


def get_totals(db_path=None):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name, count FROM totals ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    exhibits = next((count for name, count in rows if name == 'Экспонаты'), 0)
    articles = next((count for name, count in rows if name == 'Статьи'), 0)
    return exhibits, articles