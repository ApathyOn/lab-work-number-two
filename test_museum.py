# test_museum.py
import os
import sqlite3
from exhibit import Exhibit
from article import Article
from db import init_db, save_totals, get_totals


TEST_DB = "test_museum_summary.db"


def setup_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def teardown_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_exhibit_str_repr():
    exh = Exhibit("Динозавр", 100)
    assert str(exh) == "Экспонат «Динозавр» — 100 человек"
    assert repr(exh) == "Exhibit(title='Динозавр', views=100)"


def test_article_str_repr():
    art = Article("История музея", 50)
    assert str(art) == "Статья «История музея» — 50 человек"
    assert repr(art) == "Article(title='История музея', views=50)"


def test_db_init_creates_table():
    init_db(TEST_DB)
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='totals';")
    assert cur.fetchone() is not None

    cur.execute("SELECT id, name, count FROM totals ORDER BY id")
    rows = cur.fetchall()
    assert len(rows) == 2
    assert rows[0] == (1, 'Экспонаты', 0)
    assert rows[1] == (2, 'Статьи', 0)
    conn.close()


def test_save_and_get_totals():
    init_db(TEST_DB)
    save_totals(350, 120, TEST_DB)
    exhibits, articles = get_totals(TEST_DB)
    assert exhibits == 350
    assert articles == 120


def test_save_totals_updates_existing():
    init_db(TEST_DB)
    save_totals(100, 200, TEST_DB)
    save_totals(300, 400, TEST_DB)
    exhibits, articles = get_totals(TEST_DB)
    assert exhibits == 300
    assert articles == 400