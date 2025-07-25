"""Простейшая реализация Q-learning для NPC."""

from __future__ import annotations

from typing import Hashable, Iterable, List

import numpy as np


class QLearningNPC:
    """NPC, обучающийся с использованием табличного Q-learning."""

    def __init__(self, actions: Iterable[Hashable], lr: float = 0.1, gamma: float = 0.95, epsilon: float = 0.1) -> None:
        self.actions: List[Hashable] = list(actions)
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table: dict[tuple, np.ndarray] = {}

    def _ensure_state(self, state: Iterable) -> tuple:
        key = tuple(state)
        if key not in self.q_table:
            self.q_table[key] = np.zeros(len(self.actions))
        return key

    def choose_action(self, state: Iterable) -> Hashable:
        """Выбрать действие для заданного состояния."""
        key = self._ensure_state(state)
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        return self.actions[int(np.argmax(self.q_table[key]))]

    def update(self, state: Iterable, action: Hashable, reward: float, next_state: Iterable) -> None:
        """Обновить таблицу Q по наблюдению."""
        key = self._ensure_state(state)
        next_key = self._ensure_state(next_state)
        action_idx = self.actions.index(action)
        best_next = float(np.max(self.q_table[next_key]))
        target = reward + self.gamma * best_next
        self.q_table[key][action_idx] = (1 - self.lr) * self.q_table[key][action_idx] + self.lr * target
