from __future__ import annotations

import random
from typing import Dict, List


class ABTestManager:
    """Управление простыми A/B-экспериментами."""

    def __init__(self, variants: List[str]):
        if len(variants) < 2:
            raise ValueError("Нужно минимум два варианта")
        self.variants = variants
        self.exposures: Dict[str, int] = {v: 0 for v in variants}

    def assign_variant(self, user_id: str) -> str:
        """Возвращает вариант для пользователя и считает показ."""
        variant = random.choice(self.variants)
        self.exposures[variant] += 1
        return variant

    def summary(self) -> Dict[str, int]:
        return dict(self.exposures)
