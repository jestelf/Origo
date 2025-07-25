"""Простейшая стохастическая политика на основе логистической регрессии."""

from __future__ import annotations

from typing import Iterable

import numpy as np


class LogisticPolicyNPC:
    """NPC, выбирающий действия при помощи мультиклассовой логистической регрессии."""

    def __init__(self, state_dim: int, num_actions: int, lr: float = 0.1) -> None:
        self.W = np.zeros((state_dim, num_actions))
        self.lr = lr
        self.num_actions = num_actions

    def _softmax(self, z: np.ndarray) -> np.ndarray:
        e = np.exp(z - np.max(z))
        return e / e.sum()

    def choose_action(self, state: Iterable[float]) -> int:
        """Вернуть индекс выбранного действия."""
        state_vec = np.asarray(state)
        probs = self._softmax(state_vec @ self.W)
        return int(np.random.choice(self.num_actions, p=probs))

    def update(self, state: Iterable[float], action: int) -> None:
        """Обновить параметры модели одним наблюдением."""
        state_vec = np.asarray(state)
        probs = self._softmax(state_vec @ self.W)
        grad = -np.outer(state_vec, probs)
        grad[:, action] += state_vec
        self.W += self.lr * grad
