"""Инструмент мониторинга FPS и системных ресурсов."""

from __future__ import annotations

import os
import time
from typing import Dict

import psutil


class PerformanceMonitor:
    """Собирает базовые метрики производительности."""

    def __init__(self) -> None:
        self.proc = psutil.Process(os.getpid())
        self.frame_start = 0.0
        self.fps = 0.0
        self.cpu_percent = 0.0
        self.memory = 0
        self.subsystems: Dict[str, float] = {}
        self._sub_start: Dict[str, float] = {}

    def start_frame(self) -> None:
        self.frame_start = time.perf_counter()
        self.subsystems.clear()
        self._sub_start.clear()

    def end_frame(self) -> None:
        dt = time.perf_counter() - self.frame_start
        if dt > 0:
            self.fps = 1.0 / dt
        self.cpu_percent = psutil.cpu_percent(interval=None)
        self.memory = self.proc.memory_info().rss

    def start_subsystem(self, name: str) -> None:
        self._sub_start[name] = time.perf_counter()

    def end_subsystem(self, name: str) -> None:
        start = self._sub_start.pop(name, None)
        if start is not None:
            self.subsystems[name] = time.perf_counter() - start

    def report(self) -> str:
        parts = [
            f"FPS: {self.fps:.2f}",
            f"CPU: {self.cpu_percent:.1f}%",
            f"Memory: {self.memory / (1024 * 1024):.1f} MB",
        ]
        for name, t in self.subsystems.items():
            parts.append(f"{name}: {t * 1000:.2f} ms")
        return " | ".join(parts)
