from __future__ import annotations

"""Минимальная поддержка VR и AR-рендеринга."""

from dataclasses import dataclass
import logging

from origo3d.rendering.renderer import Renderer
from origo3d.input.vr import XRInput


@dataclass
class XRDisplayInfo:
    """Параметры дисплея VR/AR-устройства."""

    width: int
    height: int
    ar: bool = False


class XRRenderer(Renderer):
    """Рендерер с базовой поддержкой VR/AR."""

    def __init__(self, display_info: XRDisplayInfo) -> None:
        super().__init__(width=display_info.width, height=display_info.height)
        self.logger = logging.getLogger(__name__)
        self.display_info = display_info
        mode = "AR" if display_info.ar else "VR"
        self.logger.info("%s renderer initialized (%sx%s)", mode, display_info.width, display_info.height)

    def render_frame(self) -> None:  # pragma: no cover - зависит от среды
        """Отрисовать кадр для VR/AR-устройства."""
        self.logger.debug("XR render frame: mode=%s", "AR" if self.display_info.ar else "VR")
        super().render_frame()

    def update_from_input(self, xr_input: XRInput) -> None:
        """Обновить камеру по данным шлема."""
        self.camera.update_from_headset(xr_input.headset)
