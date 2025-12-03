# tests/test_app.py
import pytest
from app.generators import city_generator, random_tuple_gen, iterate_single_thread, iterate_threaded, words_to_table_3cols

def test_city_generator_cycle_and_length():
    cities = ["A", "B", "C"]
    gen = city_generator(cities, total=6)
    assert [next(gen) for _ in range(6)] == ["A", "B", "C", "A", "B", "C"]

def test_city_generator_invalid():
    with pytest.raises(TypeError):
        city_generator("not a list")
    with pytest.raises(ValueError):
        city_generator([], total=10)

def test_random_tuple_gen():
    g = random_tuple_gen(3, -5, 5)
    t = next(g)
    assert isinstance(t, tuple) and len(t) == 3
    assert all(isinstance(x, int) and -5 <= x <= 5 for x in t)

def test_words_to_table_3cols():
    text = "a b c d e f g h i"
    rows = words_to_table_3cols(text)
    assert rows == [("a","b","c"), ("d","e","f"), ("g","h","i")]

def test_bench_functions_return_time():
    cities = ["A","B"]
    t1 = iterate_single_thread(cities, total=1000)
    t2 = iterate_threaded(cities, total=1000, threads=2)
    assert t1 >= 0
    assert t2 >= 0
