from __future__ import annotations

"""Высокоуровневый рендерер с выбором графического API."""

from typing import Any
import logging

from hotreload.hotreloader import HotReloader
from .backends import OpenGLBackend, VulkanBackend, DirectXBackend
from origo3d.resources.shader_manager import ShaderManager


class Renderer:
    """Выбирает подходящий backend рендеринга."""

    _BACKENDS = {
        "opengl": OpenGLBackend,
        "vulkan": VulkanBackend,
        "directx": DirectXBackend,
    }

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        api: str = "opengl",
        reloader: HotReloader | None = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        backend_cls = self._BACKENDS.get(api.lower())
        if backend_cls is None:
            raise ValueError(f"Unknown graphics API: {api}")
        self.logger.info("Using %s backend", api)
        self.shader_manager = ShaderManager(reloader=reloader)
        self.backend = backend_cls(width=width, height=height, shader_manager=self.shader_manager)

    def __getattr__(self, item: str) -> Any:  # pragma: no cover - delegation
        return getattr(self.backend, item)

    def render_frame(self) -> None:
        self.backend.render_frame()
