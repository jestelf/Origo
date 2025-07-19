"""Простейший рендерер на базе :mod:`moderngl`.

На данном этапе используется минимальный набор функций:
* инициализация контекста OpenGL,
* компиляция базовых вершинного и фрагментного шейдеров,
* загрузка тестовой модели и вывод её на экран при помощи камеры.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import logging
import numpy as np

import moderngl
from origo3d.rendering.camera import Camera
from origo3d.resources.model_manager import ModelManager

from origo3d.shaders import FRAGMENT_SHADER_SOURCE, VERTEX_SHADER_SOURCE


class Renderer:
    """Создаёт контекст рендера и выводит тестовую модель."""

    def __init__(self, width: int = 800, height: int = 600) -> None:
        self.logger = logging.getLogger(__name__)
        try:
            # ``moderngl.create_context`` использует активный OpenGL-контекст
            self.ctx = moderngl.create_context()
        except Exception:  # pragma: no cover - зависит от среды
            # В тестах контекст окна отсутствует, поэтому создаём автономный
            self.logger.info("Standalone EGL context")
            self.ctx = moderngl.create_standalone_context(backend="egl")

        self.clear_color: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0)

        self.camera = Camera()
        self.camera.set_aspect(width, height)
        self.model_manager = ModelManager()
        # Компиляция простейших шейдеров
        self.program = self.ctx.program(
            vertex_shader=VERTEX_SHADER_SOURCE,
            fragment_shader=FRAGMENT_SHADER_SOURCE,
        )
        self.logger.info("Shaders compiled successfully")

        model_path = Path("assets/models/cube.obj")
        vertices = self.model_manager.load_obj(model_path).reshape(-1, 3)
        colors = np.tile(np.array([0.8, 0.3, 0.3], dtype="f4"), (len(vertices), 1))
        data = np.hstack([vertices, colors]).astype("f4").ravel()
        self.vbo = self.ctx.buffer(data.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, "3f 3f", "in_position", "in_color")],
        )

    def render_frame(self) -> None:
        """Очистить экран и нарисовать загруженную модель."""
        r, g, b, a = self.clear_color
        self.ctx.clear(r, g, b, a)
        mvp = self.camera.mvp_matrix().astype("f4")
        self.program["u_mvp"].write(mvp.tobytes())

        self.vao.render(moderngl.TRIANGLES)

