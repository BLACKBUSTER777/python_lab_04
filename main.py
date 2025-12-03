# main.py
from app.generators import city_generator, random_tuple_gen, words_to_table_3cols

def task1_cli():
    cities = ["Москва", "Ульяновск", "Самара", "Уфа", "Омск", "Тула"]
    gen = city_generator(cities, total=1000000)
    print("Первые 20 городов:")
    for _ in range(20):
        print(next(gen), end=" ")
    print("\n")

def task2_cli():
    gen = random_tuple_gen(20, -5, 5)
    matrix = [next(gen) for _ in range(20)]
    print("Матрица 20x20:")
    for row in matrix:
        print(" ".join(f"{v:2d}" for v in row))
    print()

def task3_cli():
    s = input("Введите строку слов через пробел:\n> ")
    try:
        rows = words_to_table_3cols(s)
        print("Таблица 3 столбца:")
        for row in rows:
            print(" ".join(row))
    except Exception as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    task1_cli()
    task2_cli()
    task3_cli()
