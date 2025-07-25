"""Модули для обучения поведения NPC."""

from .qlearning_npc import QLearningNPC
from .logistic_policy import LogisticPolicyNPC

__all__ = ["QLearningNPC", "LogisticPolicyNPC"]
