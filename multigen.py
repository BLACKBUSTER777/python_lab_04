# multigen.py
from app.generators import iterate_single_thread, iterate_threaded

if __name__ == "__main__":
    cities = ["Москва", "Ульяновск", "Самара", "Уфа", "Омск", "Тула"]
    total = 1000000
    threads = 4

    t_single = iterate_single_thread(cities, total=total)
    t_multi = iterate_threaded(cities, total=total, threads=threads)

    print(f"Total: {total}")
    print(f"Single-thread time: {t_single:.4f}s")
    print(f"Multi-thread ({threads}) time: {t_multi:.4f}s")
    if t_multi > 0:
        print(f"Speedup: x{t_single/t_multi:.2f}")
