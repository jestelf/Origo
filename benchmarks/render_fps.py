"""Измеряет средний FPS рендера за 10 секунд."""
from __future__ import annotations

import time
from pathlib import Path

from origo3d.rendering import Renderer

DURATION = 10.0


def run_benchmark(duration: float = DURATION) -> float:
    """Рендерит кадры в течение ``duration`` секунд и возвращает средний FPS."""
    try:
        renderer = Renderer()
    except Exception as exc:  # pragma: no cover - зависит от окружения
        print(f"Не удалось инициализировать рендерер: {exc}")
        return 0.0

    frames = 0
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
        renderer.render_frame()
        frames += 1
    total = time.perf_counter() - start
    return frames / total if total > 0 else 0.0


if __name__ == "__main__":
    fps = run_benchmark()
    print(f"Средний FPS за {int(DURATION)} секунд: {fps:.2f}")
    results = Path(__file__).parent / "results"
    results.mkdir(exist_ok=True)
    with (results / "render_fps.txt").open("w", encoding="utf-8") as f:
        f.write(f"{fps:.2f}\n")
