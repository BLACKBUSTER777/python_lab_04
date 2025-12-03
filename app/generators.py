# app/generators.py
from itertools import cycle
from random import randint
from concurrent.futures import ThreadPoolExecutor
import time

# -------------------------
# Задание 1: генератор городов
# -------------------------
def city_generator(cities, total=1000000):
    """
    Генератор, циклически выдаёт элементы из списка cities до total элементов.
    """
    if not isinstance(cities, (list, tuple)):
        raise TypeError("cities должен быть списком или кортежем")
    if len(cities) == 0:
        raise ValueError("cities не должен быть пустым")
    if not all(isinstance(c, str) for c in cities):
        raise ValueError("Все элементы в cities должны быть строками")
    if not isinstance(total, int) or total < 0:
        raise ValueError("total должен быть неотрицательным целым")


    def _gen():
        i = 0
        for item in cycle(cities):
            if i >= total:
                break
            yield item
            i += 1
    return _gen()

# -------------------------
# Задание 2
# -------------------------
def random_tuple_gen(n, a, b):
    """
    Генератор, выдаёт кортежи длины n со случайными int в [a, b].
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n должно быть положительным целым")
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a и b должны быть целыми числами")
    if a > b:
        raise ValueError("a должно быть <= b")

    while True:
        yield tuple(randint(a, b) for _ in range(n))

# -------------------------
# Задание 3
# -------------------------
def words_to_table_3cols(text):
    """
    Принимает строку слов через пробел и возвращает список кортежей по 3 слова.
    Лишние слова (не вошедшие в полную тройку) отбрасываются.
    Используется zip(*(iter(words),)*3).
    """
    if not isinstance(text, str):
        raise TypeError("Ожидается строка")
    words = text.split()
    if len(words) < 3:
        raise ValueError("Нужно минимум 3 слова")
    rows = list(zip(*(iter(words),) * 3))
    return rows
# -------------------------
# Функции для бенчмарка (однопоточный и многопоточный итератор)
# -------------------------
def iterate_single_thread(cities, total=1000000):
    """
    Просто пройтись циклически total раз (один поток). Возвращает время в сек.
    """
    if not isinstance(total, int) or total < 0:
        raise ValueError("total должен быть неотрицательным целым")
    start = time.perf_counter()
    for _, _ in zip(range(total), cycle(cities)):
        pass
    end = time.perf_counter()
    return end - start

def _worker_cycle(cities, count):
    """Воркер для потока — просто итерация count раз."""
    for _, _ in zip(range(count), cycle(cities)):
        pass

def iterate_threaded(cities, total=1000000, threads=4):
    """
    Многопоточный перебор — разбиваем total на threads частей.
    Возвращает время в секундах.
    """
    if not isinstance(threads, int) or threads <= 0:
        raise ValueError("threads должен быть положительным целым")
    if total < 0:
        raise ValueError("total должен быть неотрицательным")
    if threads == 1:
        return iterate_single_thread(cities, total=total)

    chunk = total // threads
    remainder = total - chunk * threads

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = []
        for i in range(threads):
            cnt = chunk + (1 if i < remainder else 0)
            futures.append(ex.submit(_worker_cycle, cities, cnt))
        for f in futures:
            f.result()
    end = time.perf_counter()
    return end - start

