import os
import sqlite3
import pytest
from db import init_db, get_all_items, add_rating
from main import export_report

TEST_DB = "test_museum.db"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_db(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_db_structure_created():
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
    assert cur.fetchone() is not None, "Таблица items не создана"

    cur.execute("PRAGMA table_info(items)")
    columns = [c[1] for c in cur.fetchall()]
    for col in ("id", "type", "title", "avg_rating", "num_ratings", "position"):
        assert col in columns, f"Отсутствует колонка {col}"
    conn.close()


def test_add_rating_and_average_calculation():
    items_before = get_all_items(TEST_DB)
    item_id = items_before[0][0]
    add_rating(item_id, 8, TEST_DB)
    add_rating(item_id, 6, TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT avg_rating, num_ratings FROM items WHERE id=?", (item_id,))
    avg, count = cur.fetchone()
    conn.close()

    assert count == 2
    assert round(avg, 2) == 7.0


def test_add_rating_invalid_id():
    with pytest.raises(ValueError):
        add_rating(9999, 5, TEST_DB)


def test_add_rating_invalid_value_type():
    items = get_all_items(TEST_DB)
    with pytest.raises(TypeError):
        add_rating(items[0][0], "abc", TEST_DB)


def test_add_rating_out_of_range():
    items = get_all_items(TEST_DB)
    with pytest.raises(ValueError):
        add_rating(items[0][0], 15, TEST_DB)


def test_items_sorted_by_avg_rating():
    items = get_all_items(TEST_DB)
    add_rating(items[0][0], 2, TEST_DB)
    add_rating(items[1][0], 9, TEST_DB)
    add_rating(items[2][0], 6, TEST_DB)
    sorted_items = get_all_items(TEST_DB)
    ratings = [item[3] for item in sorted_items]  
    assert ratings == sorted(ratings, reverse=True), "Сортировка по avg_rating неверна"


def test_export_files_created(tmp_path):
    items = get_all_items(TEST_DB)
    os.chdir(tmp_path)
    export_report(items)
    assert os.path.exists("museum_summary_report.docx"), "Файл Word не создан"
    assert os.path.exists("museum_summary_report.xlsx"), "Файл Excel не создан"


def test_multiple_items_average_update():
    items = get_all_items(TEST_DB)
    id1, id2 = items[0][0], items[1][0]
    add_rating(id1, 10, TEST_DB)
    add_rating(id2, 5, TEST_DB)
    add_rating(id1, 0, TEST_DB)
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT avg_rating FROM items WHERE id=?", (id1,))
    avg1 = cur.fetchone()[0]
    cur.execute("SELECT avg_rating FROM items WHERE id=?", (id2,))
    avg2 = cur.fetchone()[0]
    conn.close()
    assert round(avg1, 2) == 5.0 and round(avg2, 2) == 5.0, "Средние значения пересчитаны неверно"


def test_init_db_recreates_missing_table():
    os.remove(TEST_DB)
    init_db(TEST_DB)
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items")
    count = cur.fetchone()[0]
    conn.close()
    assert count > 0, "После повторной инициализации таблица не создана"


def test_get_all_items_returns_expected_format():
    items = get_all_items(TEST_DB)
    assert isinstance(items, list)
    assert all(isinstance(i, tuple) for i in items)
    assert len(items[0]) == 6, "Каждый объект должен иметь 6 полей (id, type, title, avg_rating, num_ratings, position)"
