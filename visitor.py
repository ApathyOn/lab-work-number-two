# visitor.py
from base import log_action
import sqlite3

class Visitor:
    def __init__(self, visitor_id, name="Аноним"):
        self.id = visitor_id
        self.name = name

    @log_action("Посетитель взаимодействует")
    def view(self, item, watch_time_sec):
        item.add_view(self.id, watch_time_sec)

    def get_stats(self):
        conn = sqlite3.connect("museum.db")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), SUM(watch_time) FROM views WHERE visitor_id = ?", (self.id,))
        count, total = cur.fetchone()
        conn.close()
        total = total or 0.0
        avg = total / count if count > 0 else 0.0
        return int(count or 0), total, avg

    def __str__(self):
        views, total, avg = self.get_stats()
        return f"Посетитель {self.name} ({self.id}): {views} просмотров, всего {total:.1f} сек"

    def __repr__(self):
        return f"Visitor(id='{self.id}', name='{self.name}')"