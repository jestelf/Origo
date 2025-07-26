"""Измеряет время создания 1000 сущностей через систему ECS."""
from __future__ import annotations

import time
from pathlib import Path

from origo3d.ecs.entity_manager import EntityManager


COUNT = 1000


def run_benchmark(n: int = COUNT) -> float:
    """Создать ``n`` сущностей и вернуть затраченное время в секундах."""
    manager = EntityManager()
    start = time.perf_counter()
    for i in range(n):
        manager.create_entity(f"ent_{i}")
    return time.perf_counter() - start


if __name__ == "__main__":
    duration = run_benchmark()
    print(f"Создание {COUNT} сущностей заняло {duration:.6f} с")
    results = Path(__file__).parent / "results"
    results.mkdir(exist_ok=True)
    with (results / "entity_spawn_perf.txt").open("w", encoding="utf-8") as f:
        f.write(f"{duration:.6f}\n")
