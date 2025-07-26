from __future__ import annotations

"""Заглушка для DirectX."""

from typing import Tuple
import logging

from origo3d.rendering.camera import Camera
from origo3d.resources.shader_manager import ShaderManager
from origo3d.shaders import get_shader_sources


class DirectXBackend:
    """Заглушка реализации DirectX."""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        shader_manager: ShaderManager | None = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.warning("DirectX backend not fully implemented")
        self.clear_color: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0)
        self.camera = Camera()
        self.camera.set_aspect(width, height)
        self.program = None
        self.vbo = None
        _ = get_shader_sources("directx")

    def render_frame(self) -> None:
        self.logger.debug("DirectXBackend.render_frame called")
