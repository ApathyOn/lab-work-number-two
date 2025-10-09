# main.py
from exhibit import Exhibit
from article import Article
from db import init_db, save_totals, get_totals, DEFAULT_DB_PATH
from docx import Document
from openpyxl import Workbook


def export_report(total_exhibits, total_articles):
    total_all = total_exhibits + total_articles

    # DOCX
    doc = Document()
    doc.add_heading('Итоговый отчёт: Виртуальный музей', 0)
    doc.add_paragraph(f"Общее число людей, посмотревших ЭКСПОНАТЫ: {total_exhibits}")
    doc.add_paragraph(f"Общее число людей, посмотревших СТАТЬИ:    {total_articles}")
    doc.add_paragraph(f"ВСЕГО:                                    {total_all}")
    doc.save('museum_summary_report.docx')

    # XLSX
    wb = Workbook()
    ws = wb.active
    ws.append(["Категория", "Количество человек"])
    ws.append(["Экспонаты", total_exhibits])
    ws.append(["Статьи", total_articles])
    ws.append(["Всего", total_all])
    wb.save('museum_summary_report.xlsx')

def main():
    init_db()
    total_exhibits = 0
    total_articles = 0

    print("🏛️ Ввод данных о просмотрах")
    print("Введите информацию по каждому объекту. Завершите ввод командой 'стоп'.\n")

    while True:
        choice = input("Тип объекта (1 — Экспонат, 2 — Статья, 'стоп' — завершить): ").strip()
        if choice.lower() in ('стоп', 'stop', 'q'):
            break
        if choice not in ('1', '2'):
            print("Введите 1, 2 или 'стоп'.")
            continue

        title = input("Название: ").strip()
        if not title:
            print("Название не может быть пустым.")
            continue

        try:
            views = int(input("Сколько человек посмотрело? "))
            if views < 0:
                print("Число не может быть отрицательным.")
                continue
        except ValueError:
            print("Введите целое число.")
            continue

        # Создаём объект (для демонстрации ООП)
        if choice == "1":
            item = Exhibit(title, views)
            total_exhibits += views
        else:
            item = Article(title, views)
            total_articles += views

        print(f"✅ Учтено: {item}\n")

    # Сохраняем ТОЛЬКО итоги в БД
    save_totals(total_exhibits, total_articles)

    # Вывод результата
    total_all = total_exhibits + total_articles
    print("\n" + "="*50)
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print("="*50)
    print(f"Экспонаты: {total_exhibits} человек")
    print(f"Статьи:    {total_articles} человек")
    print(f"Всего:     {total_all} человек")

    # Экспорт отчёта
    export_report(total_exhibits, total_articles)
    print("\n✅ Отчёт сохранён: museum_summary_report.docx, museum_summary_report.xlsx")
    print("✅ Итоги сохранены в: museum_summary.db")

if __name__ == "__main__":
    main()