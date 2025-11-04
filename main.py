from db import init_db, get_all_items, add_rating

def main():
    init_db()
    print("Добро пожаловать в Виртуальный музей!")
    print("Оцените объекты от 0 до 10.\n")

    while True:
        items = get_all_items()
        print("=" * 85)
        print(f"{'ID':<4} {'Тип':<10} {'Название':<45} {'Средняя':<10} {'Кол-во'}")
        print("=" * 85)
        for item_id, type_, title, avg_rating, num_ratings, position in items:
            print(f"{item_id:<4} {type_:<10} {title:<45} {avg_rating:>7.2f} {num_ratings:>7}")
        print("=" * 85)

        choice = input("\nВведите ID объекта для оценки (или 'стоп' для выхода): ").strip()
        if choice.lower() in ('стоп', 'stop', 'q'):
            break

        try:
            item_id = int(choice)
        except ValueError:
            print("Введите корректный номер ID.")
            continue

        valid_ids = [row[0] for row in items]
        if item_id not in valid_ids:
            print("Объект с таким ID не найден.")
            continue

        rating_input = input("Введите оценку (0–10): ").strip()
        try:
            rating = int(rating_input)
            if not (0 <= rating <= 10):
                print("Оценка должна быть от 0 до 10.")
                continue
        except ValueError:
            print("Введите число.")
            continue

        add_rating(item_id, rating)
        print("Оценка сохранена и таблица обновлена!\n")

    print("\nИтоговая таблица:")
    for item_id, type_, title, avg_rating, num_ratings, position in get_all_items():
        print(f"{type_:<10} | {title:<45} | Средняя: {avg_rating:>5.2f} ({num_ratings} оценок)")
    print("=" * 85)
    print("Работа завершена!")

if __name__ == "__main__":
    main()
