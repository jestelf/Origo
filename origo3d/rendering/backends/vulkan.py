from __future__ import annotations

"""Временный заглушка для Vulkan."""

from typing import Tuple
import logging

from origo3d.rendering.camera import Camera
from origo3d.resources.shader_manager import ShaderManager
from origo3d.shaders import get_shader_sources


class VulkanBackend:
    """Заглушка реализации Vulkan."""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        shader_manager: ShaderManager | None = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.warning("Vulkan backend not fully implemented")
        self.clear_color: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 1.0)
        self.camera = Camera()
        self.camera.set_aspect(width, height)
        self.program = None
        self.vbo = None
        _ = get_shader_sources("vulkan")

    def render_frame(self) -> None:
        self.logger.debug("VulkanBackend.render_frame called")
