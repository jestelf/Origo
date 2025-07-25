"""Утилита для компиляции шейдера и рендера предпросмотра материала."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import moderngl
import numpy as np

from origo3d.rendering.camera import Camera
from origo3d.resources.model_manager import ModelManager
from .pbr_shader import PBR_VERTEX_SHADER, PBR_FRAGMENT_SHADER


class ShaderPreview:
    """Создаёт offscreen-буфер и рисует сферу с заданным материалом."""

    def __init__(self, width: int = 256, height: int = 256) -> None:
        self.size = (width, height)
        try:
            self.ctx = moderngl.create_context()
        except Exception:  # pragma: no cover - зависит от среды
            try:
                self.ctx = moderngl.create_standalone_context(backend="egl")
            except Exception:  # pragma: no cover - среда без GL/EGL
                self.ctx = None

        if self.ctx:
            self.fbo = self.ctx.simple_framebuffer(self.size)
            self.fbo.use()
        else:
            self.fbo = None

        self.camera = Camera()
        self.camera.set_aspect(width, height)
        self.model_manager = ModelManager()

        # Используем простую модель куба для предпросмотра
        model_path = Path("assets/models/cube.obj")
        if self.ctx:
            vertices = self.model_manager.load_obj(model_path).reshape(-1, 3)
            normals = np.tile(np.array([0.0, 0.0, 1.0], dtype="f4"), (len(vertices), 1))
            data = np.hstack([vertices, normals]).astype("f4").ravel()
            self.vbo = self.ctx.buffer(data.tobytes())

            self.program = self.ctx.program(
                vertex_shader=PBR_VERTEX_SHADER,
                fragment_shader=PBR_FRAGMENT_SHADER,
            )
            self.vao = self.ctx.vertex_array(
                self.program,
                [(self.vbo, "3f 3f", "in_position", "in_normal")],
            )
            self.ctx.enable(moderngl.DEPTH_TEST)

    def render(
        self,
        albedo: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        metallic: float = 0.0,
        roughness: float = 0.5,
    ) -> bytes:
        """Рендерит сферу и возвращает RGB-данные."""
        if not self.ctx:
            return bytes(self.size[0] * self.size[1] * 3)

        self.fbo.clear(0.0, 0.0, 0.0, 1.0, depth=1.0)
        mvp = self.camera.mvp_matrix().astype("f4")
        self.program["u_mvp"].write(mvp.tobytes())
        self.program["u_albedo"].value = tuple(albedo)
        self.program["u_metallic"].value = float(metallic)
        self.program["u_roughness"].value = float(roughness)
        self.vao.render(moderngl.TRIANGLES)
        return self.fbo.read(components=3)
