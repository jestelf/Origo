"""Примеры использования моделей обучения поведения NPC."""

from __future__ import annotations

import numpy as np

from origo3d.ai.ml import LogisticPolicyNPC, QLearningNPC


def qlearning_example() -> None:
    """Демонстрация табличного Q-learning."""
    actions = ["идти", "стоять"]
    agent = QLearningNPC(actions)
    state = [0]
    for _ in range(10):
        action = agent.choose_action(state)
        reward = 1.0 if action == "идти" else 0.0
        next_state = [state[0] + 1]
        agent.update(state, action, reward, next_state)
        state = next_state
    print("Q-таблица:", agent.q_table)


def logistic_example() -> None:
    """Пример обучения логистической политики."""
    agent = LogisticPolicyNPC(state_dim=1, num_actions=2)
    # Учим выбирать действие 1, если значение состояния > 0.5
    for _ in range(50):
        s = np.random.rand(1)
        a = 1 if s[0] > 0.5 else 0
        agent.update(s, a)
    test_state = np.array([0.8])
    chosen = agent.choose_action(test_state)
    print("Логистическая политика выбрала:", chosen)


if __name__ == "__main__":
    qlearning_example()
    logistic_example()
