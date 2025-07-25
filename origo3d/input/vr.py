from __future__ import annotations

"""Ввод с VR-шлемов и AR-устройств."""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ControllerState:
    """Положение и ориентация контроллера."""

    position: Tuple[float, float, float]
    orientation: Tuple[float, float, float]


@dataclass
class HeadsetState:
    """Положение и ориентация шлема."""

    position: Tuple[float, float, float]
    orientation: Tuple[float, float, float]


class XRInput:
    """Сбор данных о состоянии VR/AR-устройств."""

    def __init__(self) -> None:
        self.headset = HeadsetState((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        self.controllers: list[ControllerState] = []

    def poll(self) -> None:  # pragma: no cover - взаимодействие с оборудованием
        """Обновить состояние устройств."""
        # Заглушка: в реальном движке здесь использовалась бы библиотека OpenXR
        # или драйвер конкретного устройства.
        pass
