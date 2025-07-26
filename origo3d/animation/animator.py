"""Простейший компонент анимации."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Animator:
    """Хранит текущее время анимации и обновляет его."""

    time: float = 0.0

    def update(self, dt: float) -> None:
        self.time += dt