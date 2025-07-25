from __future__ import annotations

"""Простейшая камера с перспективной проекцией."""

from dataclasses import dataclass, field

import numpy as np
from pyrr import Vector3, matrix44


@dataclass
class Camera:
    """Камера со стандартными параметрами проекции."""

    fov: float = 60.0
    aspect: float = 4 / 3
    near: float = 0.1
    far: float = 100.0
    position: Vector3 = field(default_factory=lambda: Vector3([0.0, 0.0, 3.0]))
    target: Vector3 = field(default_factory=lambda: Vector3([0.0, 0.0, 0.0]))
    up: Vector3 = field(default_factory=lambda: Vector3([0.0, 1.0, 0.0]))

    def projection_matrix(self) -> np.ndarray:
        """Возвращает матрицу перспективной проекции."""
        return matrix44.create_perspective_projection(
            self.fov, self.aspect, self.near, self.far, dtype="f4"
        )

    def view_matrix(self) -> np.ndarray:
        """Возвращает матрицу вида."""
        return matrix44.create_look_at(self.position, self.target, self.up, dtype="f4")

    def mvp_matrix(self) -> np.ndarray:
        """Матрица вида-проекции."""
        return self.projection_matrix() @ self.view_matrix()

    def set_aspect(self, width: int, height: int) -> None:
        """Обновить соотношение сторон экрана."""
        self.aspect = width / float(height)

    def update_from_headset(self, headset: "HeadsetState") -> None:
        """Синхронизировать камеру с положением VR/AR-шлема."""
        self.position = Vector3(headset.position)
        pitch, yaw, _ = headset.orientation
        forward = Vector3([
            np.cos(pitch) * np.sin(yaw),
            np.sin(pitch),
            np.cos(pitch) * np.cos(yaw),
        ])
        self.target = self.position + forward
