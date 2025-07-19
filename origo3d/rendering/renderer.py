"""Простейший рендерер на базе :mod:`moderngl`.

На данном этапе используется минимальный набор функций:
* инициализация контекста OpenGL,
* компиляция базовых вершинного и фрагментного шейдеров,
* вывод на экран тестового треугольника.
"""

from __future__ import annotations

from typing import Tuple

import logging
import numpy as np

import moderngl

from origo3d.shaders import FRAGMENT_SHADER_SOURCE, VERTEX_SHADER_SOURCE


class Renderer:
    """Создаёт контекст рендера и выводит тестовый треугольник."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        try:
            # ``moderngl.create_context`` использует активный OpenGL-контекст
            self.ctx = moderngl.create_context()
        except Exception:  # pragma: no cover - зависит от среды
            # В тестах контекст окна отсутствует, поэтому создаём автономный
            self.logger.info("Standalone EGL context")
            self.ctx = moderngl.create_standalone_context(backend="egl")

        self.clear_color: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0)

        # Компиляция простейших шейдеров
        self.program = self.ctx.program(
            vertex_shader=VERTEX_SHADER_SOURCE,
            fragment_shader=FRAGMENT_SHADER_SOURCE,
        )
        self.logger.info("Shaders compiled successfully")

        # Геометрия треугольника: XY + RGB
        vertices = np.array(
            [
                -0.6,
                -0.6,
                1.0,
                0.0,
                0.0,
                0.6,
                -0.6,
                0.0,
                1.0,
                0.0,
                0.0,
                0.6,
                0.0,
                0.0,
                1.0,
            ],
            dtype="f4",
        )
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, "2f 3f", "in_position", "in_color")],
        )

    def render_frame(self) -> None:
        """Очистить экран и нарисовать тестовый треугольник."""
        r, g, b, a = self.clear_color
        self.ctx.clear(r, g, b, a)
        self.vao.render(moderngl.TRIANGLES)

