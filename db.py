import sqlite3
from typing import Optional

DEFAULT_DB_PATH = "museum_summary.db"
EPSILON = 1e-9


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    return sqlite3.connect(db_path or DEFAULT_DB_PATH)


def init_db(db_path: Optional[str] = None) -> None:
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            avg_rating REAL DEFAULT 0,
            num_ratings INTEGER DEFAULT 0,
            position INTEGER DEFAULT 0
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            value INTEGER NOT NULL CHECK(value BETWEEN 0 AND 10),
            FOREIGN KEY(item_id) REFERENCES items(id)
        )
    ''')

   
    cur.execute("SELECT COUNT(*) FROM items")
    if cur.fetchone()[0] == 0:
        items = [
            ("Экспонат", "Картина «Звёздная ночь»", 0.0, 0, 0),
            ("Экспонат", "Статуя Афродиты", 0.0, 0, 0),
            ("Статья", "История Ренессанса", 0.0, 0, 0),
            ("Статья", "Архитектура древнего Египта", 0.0, 0, 0),
        ]
        cur.executemany(
            "INSERT INTO items (type, title, avg_rating, num_ratings, position) VALUES (?, ?, ?, ?, ?)",
            items
        )

    conn.commit()
    conn.close()

    
    recompute_positions(db_path)


def _get_item_exists(cur: sqlite3.Cursor, item_id: int) -> bool:
    cur.execute("SELECT 1 FROM items WHERE id = ?", (item_id,))
    return cur.fetchone() is not None


def add_rating(item_id: int, rating: int, db_path: Optional[str] = None) -> None:
    if not isinstance(rating, (int, float)):
        raise TypeError("rating должен быть числом (int или float)")
    if rating < 0 or rating > 10:
        raise ValueError("rating должен быть в диапазоне 0..10")

    conn = get_connection(db_path)
    cur = conn.cursor()

    if not _get_item_exists(cur, item_id):
        conn.close()
        raise ValueError(f"Объект с id={item_id} не найден")

    
    cur.execute("INSERT INTO ratings (item_id, value) VALUES (?, ?)", (item_id, rating))
    conn.commit()

    
    cur.execute("SELECT SUM(value) AS s, COUNT(value) AS c FROM ratings WHERE item_id = ?", (item_id,))
    s, c = cur.fetchone()
    s = s or 0
    c = c or 0
    avg = float(s) / c if c != 0 else 0.0

    cur.execute("UPDATE items SET avg_rating = ?, num_ratings = ? WHERE id = ?", (avg, c, item_id))
    conn.commit()

   
    recompute_positions(db_path)
    conn.close()


def recompute_positions(db_path: Optional[str] = None) -> None:
    conn = get_connection(db_path)
    cur = conn.cursor()

    
    cur.execute("SELECT id FROM items ORDER BY avg_rating DESC, id ASC")
    rows = cur.fetchall()
    
    ids_in_order = [r[0] for r in rows]

    for pos, item_id in enumerate(ids_in_order, start=1):
        cur.execute("UPDATE items SET position = ? WHERE id = ?", (pos, item_id))

    conn.commit()
    conn.close()


def get_all_items(db_path: Optional[str] = None):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, type, title, avg_rating, num_ratings, position FROM items ORDER BY position ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def recalculate_all_avg(db_path: Optional[str] = None) -> None:
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT id FROM items")
    item_ids = [r[0] for r in cur.fetchall()]

    for item_id in item_ids:
        cur.execute("SELECT SUM(value) AS s, COUNT(value) AS c FROM ratings WHERE item_id = ?", (item_id,))
        s, c = cur.fetchone()
        s = s or 0
        c = c or 0
        avg = float(s) / c if c != 0 else 0.0
        cur.execute("UPDATE items SET avg_rating = ?, num_ratings = ? WHERE id = ?", (avg, c, item_id))

    conn.commit()
    conn.close()

    recompute_positions(db_path)


def verify_and_fix(db_path: Optional[str] = None) -> None:
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT id, avg_rating, num_ratings FROM items")
    items = cur.fetchall()
    issues = []

    for item_id, stored_avg, stored_count in items:
        cur.execute("SELECT SUM(value) AS s, COUNT(value) AS c FROM ratings WHERE item_id = ?", (item_id,))
        s, c = cur.fetchone()
        s = s or 0
        c = c or 0
        calc_avg = float(s) / c if c != 0 else 0.0

        if abs((stored_avg or 0.0) - calc_avg) > EPSILON or stored_count != c:
            issues.append((item_id, stored_avg, stored_count, calc_avg, c))
            cur.execute("UPDATE items SET avg_rating = ?, num_ratings = ? WHERE id = ?", (calc_avg, c, item_id))

    conn.commit()
    conn.close()

    if issues:
        recompute_positions(db_path)
        print("verify_and_fix: исправлены несоответствия для item_id:", [i[0] for i in issues])
    else:
        print("verify_and_fix: несоответствий не найдено.")


if __name__ == "__main__":
    init_db()
    verify_and_fix()
    for row in get_all_items():
        print(row)
