# ui.py
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QTabWidget, QLineEdit, QLabel, QHBoxLayout, QSpinBox, QMessageBox
)
from PySide6.QtCore import QThread, Signal
from app.generators import city_generator, random_tuple_gen, iterate_single_thread, iterate_threaded, words_to_table_3cols

class BenchWorker(QThread):
    finished_signal = Signal(float, float)  # single_time, multi_time

    def __init__(self, cities, total, threads):
        super().__init__()
        self.cities = cities
        self.total = total
        self.threads = threads

    def run(self):
        t1 = iterate_single_thread(self.cities, total=self.total)
        t2 = iterate_threaded(self.cities, total=self.total, threads=self.threads)
        self.finished_signal.emit(t1, t2)

class Task1Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.cities = ["Москва", "Ульяновск", "Самара", "Уфа", "Омск", "Тула"]
        self.total_gen = 1000000
        self.gen = city_generator(self.cities, total=self.total_gen)

        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.next_btn = QPushButton("Следующие 20")
        self.reset_btn = QPushButton("Сброс")
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.reset_btn)

        bench_layout = QHBoxLayout()
        self.total_spin = QSpinBox(); self.total_spin.setRange(1000, 5000000); self.total_spin.setValue(1000000)
        self.threads_spin = QSpinBox(); self.threads_spin.setRange(1, 64); self.threads_spin.setValue(4)
        self.bench_btn = QPushButton("Запустить benchmark (в фоне)")
        bench_layout.addWidget(QLabel("Total:")); bench_layout.addWidget(self.total_spin)
        bench_layout.addWidget(QLabel("Threads:")); bench_layout.addWidget(self.threads_spin)
        bench_layout.addWidget(self.bench_btn)

        self.out = QTextEdit(); self.out.setReadOnly(True)
        self.res_label = QLabel("Benchmark: —")

        layout.addLayout(btn_layout)
        layout.addLayout(bench_layout)
        layout.addWidget(self.res_label)
        layout.addWidget(self.out)
        self.setLayout(layout)

        self.next_btn.clicked.connect(self.show_next20)
        self.reset_btn.clicked.connect(self.reset_gen)
        self.bench_btn.clicked.connect(self.run_bench)
        self.worker = None

    def show_next20(self):
        try:
            items = [next(self.gen) for _ in range(20)]
            self.out.append(" ".join(items))
        except StopIteration:
            self.out.append("[Генератор закончился]")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def reset_gen(self):
        self.gen = city_generator(self.cities, total=self.total_gen)
        self.out.append("[Генератор сброшен]")

    def run_bench(self):
        total = int(self.total_spin.value())
        threads = int(self.threads_spin.value())
        self.res_label.setText("Benchmark: выполняется...")
        self.bench_btn.setEnabled(False)
        self.worker = BenchWorker(self.cities, total, threads)
        self.worker.finished_signal.connect(self.on_bench_finished)
        self.worker.start()

    def on_bench_finished(self, t_single, t_multi):
        self.bench_btn.setEnabled(True)
        speedup = t_single / t_multi if t_multi > 0 else float('inf')
        self.res_label.setText(f"Single: {t_single:.4f}s  Multi({self.threads_spin.value()}): {t_multi:.4f}s  Speedup: x{speedup:.2f}")
        self.out.append(f"[bench] single={t_single:.4f}s  multi={t_multi:.4f}s  speedup={speedup:.2f}")

class Task2Tab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.btn = QPushButton("Сгенерировать 20×20")
        self.out = QTextEdit(); self.out.setReadOnly(True)
        layout.addWidget(self.btn); layout.addWidget(self.out)
        self.setLayout(layout)
        self.btn.clicked.connect(self.make_matrix)

    def make_matrix(self):
        try:
            gen = random_tuple_gen(20, -5, 5)
            matrix = [next(gen) for _ in range(20)]
            self.out.setText("\n".join(" ".join(f"{v:2d}" for v in row) for row in matrix))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

class Task3Tab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.input = QLineEdit(); self.input.setPlaceholderText("Введите строку слов через пробел...")
        self.btn = QPushButton("Преобразовать")
        self.out = QTextEdit(); self.out.setReadOnly(True)
        layout.addWidget(self.input); layout.addWidget(self.btn); layout.addWidget(self.out)
        self.setLayout(layout)
        self.btn.clicked.connect(self.convert)

    def convert(self):
        try:
            text = self.input.text()
            rows = words_to_table_3cols(text)
            self.out.clear()
            for r in rows:
                self.out.append(" ".join(r))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

def run_ui():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Лабораторная — Генераторы")
    layout = QVBoxLayout()
    tabs = QTabWidget()
    tabs.addTab(Task1Tab(), "Задание 1")
    tabs.addTab(Task2Tab(), "Задание 2")
    tabs.addTab(Task3Tab(), "Задание 3")
    layout.addWidget(tabs)
    window.setLayout(layout)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_ui()
