"""Простейший визуальный редактор шейдеров с предпросмотром."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from PIL import Image

from origo3d.rendering.shader_preview import ShaderPreview


@dataclass
class ShaderParams:
    """Параметры материала для PBR."""

    albedo: Tuple[float, float, float] = (0.8, 0.8, 0.8)
    metallic: float = 0.0
    roughness: float = 0.5


class ShaderEditorGUI:
    """CLI-заглушка визуального редактора."""

    def __init__(self, width: int = 256, height: int = 256) -> None:
        self.preview = ShaderPreview(width, height)
        self.params = ShaderParams()

    def render_preview(self) -> Image.Image:
        """Компилирует материал и возвращает изображение предпросмотра."""
        data = self.preview.render(
            albedo=self.params.albedo,
            metallic=self.params.metallic,
            roughness=self.params.roughness,
        )
        return Image.frombytes("RGB", self.preview.fbo.size, data)
