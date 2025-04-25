
# Програмна реалізація Завдання-1 «Оптимізація черги 3D-принтера в університетській лабораторії»

from typing import List, Dict
from dataclasses import dataclass
from itertools import combinations

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Сортуємо завдання за зростанням пріоритету (1 - найвищий)
    jobs.sort(key=lambda x: x.priority)

    used = set()
    print_order = []
    total_time = 0

    for priority in [1, 2, 3]:
        current_jobs = [job for job in jobs if job.priority == priority and job.id not in used]
        while current_jobs:
            batch = []
            batch_volume = 0
            for job in current_jobs:
                if len(batch) < printer.max_items and batch_volume + job.volume <= printer.max_volume:
                    batch.append(job)
                    batch_volume += job.volume

            if not batch:
                # Якщо не вдалося набрати жодного завдання — беремо найбільше за обсягом, що входить
                for job in current_jobs:
                    if job.volume <= printer.max_volume:
                        batch = [job]
                        break

            if batch:
                print_order.extend([job.id for job in batch])
                total_time += max(job.print_time for job in batch)
                used.update(job.id for job in batch)

            current_jobs = [job for job in current_jobs if job.id not in used]

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування

def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
