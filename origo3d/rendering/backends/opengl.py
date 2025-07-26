from __future__ import annotations

"""OpenGL backend implemented with :mod:`moderngl`."""

from pathlib import Path
from typing import Tuple

import logging
import numpy as np
import moderngl

from origo3d.rendering.camera import Camera
from origo3d.resources.model_manager import ModelManager
from origo3d.resources.shader_manager import ShaderManager


class OpenGLBackend:
    """Рендерер OpenGL."""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        shader_manager: ShaderManager | None = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        try:
            self.ctx = moderngl.create_context()
        except Exception:  # pragma: no cover - depends on env
            self.logger.info("Standalone EGL context")
            self.ctx = moderngl.create_standalone_context(backend="egl")

        self.clear_color: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0)
        self.camera = Camera()
        self.camera.set_aspect(width, height)
        self.model_manager = ModelManager()
        self.shader_manager = shader_manager or ShaderManager()
        vert_path = Path("assets/shaders/basic.vert")
        frag_path = Path("assets/shaders/basic.frag")
        self.program = self.shader_manager.load_program(self.ctx, vert_path, frag_path)
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
        r, g, b, a = self.clear_color
        self.ctx.clear(r, g, b, a)
        mvp = self.camera.mvp_matrix().astype("f4")
        self.program["u_mvp"].write(mvp.tobytes())
        self.vao.render(moderngl.TRIANGLES)
