"""Загрузка и кеширование текстур."""

from __future__ import annotations

from pathlib import Path
from typing import Dict
from io import BytesIO

from PIL import Image

from runtime import env_settings
from .manifest import AssetManifest


class TextureManager:
    """Загружает изображения и кэширует их."""

    def __init__(self, manifest: AssetManifest | None = None) -> None:
        self.manifest = manifest or AssetManifest()
        self._textures: Dict[str, Image.Image] = {}

    def import_texture(self, path: Path) -> str:
        """Добавить текстуру в манифест и вернуть её GUID."""
        return self.manifest.import_resource(path)

    def get(self, guid: str) -> Image.Image:
        if guid in self._textures:
            return self._textures[guid]
        data = self.manifest.load(guid)
        if data is None:
            raise FileNotFoundError(f"Texture with GUID {guid} not found")
        img = Image.open(BytesIO(data)).convert("RGBA")
        if env_settings.mobile_mode():
            max_res = env_settings.get("graphics", {}).get("texture_resolution", 512)
            img.thumbnail((max_res, max_res))
        self._textures[guid] = img
        return img

    def load_texture(self, path: Path) -> Image.Image:
        """Импортировать текстуру и вернуть объект :class:`Image`."""
        guid = self.import_texture(path)
        return self.get(guid)

    def search_textures(self, keyword: str):
        """Поиск текстур по ключевому слову."""
        return self.manifest.search(keyword)
