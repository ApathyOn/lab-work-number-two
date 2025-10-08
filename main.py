# main.py
from base import init_db
from exhibit import Exhibit
from article import Article
from visitor import Visitor
from docx import Document
from openpyxl import Workbook

def export_report(items, visitors):
    # Экспорт в DOCX
    doc = Document()
    doc.add_heading('Отчёт: Виртуальный музей', 0)
    doc.add_heading('Популярность объектов', level=1)
    for item in items:
        doc.add_paragraph(str(item))
    doc.add_heading('Статистика посетителей', level=1)
    for v in visitors:
        doc.add_paragraph(str(v))
    doc.save('museum_report.docx')

    # Экспорт в XLSX
    wb = Workbook()
    ws = wb.active
    ws.title = "Популярность"
    ws.append(["Тип", "Название", "Просмотры", "Ср. время (сек)"])
    for item in items:
        views, avg = item.get_stats()
        ws.append([item.get_type_name(), item.title, views, round(avg, 1)])
    
    ws2 = wb.create_sheet("Посетители")
    ws2.append(["ID", "Имя", "Просмотров", "Общее время (сек)"])
    for v in visitors:
        views, total, _ = v.get_stats()
        ws2.append([v.id, v.name, views, round(total, 1)])
    
    wb.save('museum_report.xlsx')

def main():
    init_db()
    print("=== Виртуальный музей (Well-done, 5 файлов) ===\n")

    # Создание объектов
    exhibit = Exhibit("Золотая маска Тутанхамона")
    article = Article("Тайны древнеегипетских гробниц")

    visitor1 = Visitor("V001", "Анна")
    visitor2 = Visitor("V002", "Борис")

    # Симуляция просмотров
    visitor1.view(exhibit, 45.0)
    visitor1.view(article, 120.0)
    visitor2.view(exhibit, 60.0)
    visitor2.view(article, 90.0)

    # Вывод результатов
    print("📊 Популярность:")
    print(exhibit)
    print(article)

    print("\n👥 Посетители:")
    print(visitor1)
    print(visitor2)

    # Сохранение отчёта
    export_report([exhibit, article], [visitor1, visitor2])
    print("\n✅ Отчёт сохранён: museum_report.docx, museum_report.xlsx")
    print("✅ Данные сохранены в: museum.db")

if __name__ == "__main__":
    main()