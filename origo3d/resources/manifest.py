"""Хранение и поиск ресурсов по GUID."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional


class AssetManifest:
    """Простое хранилище соответствий GUID -> путь к файлу."""

    def __init__(self, manifest_file: Path | str = "assets/manifest.json") -> None:
        self.manifest_file = Path(manifest_file)
        self._registry: Dict[str, str] = {}
        self._cache: Dict[str, bytes] = {}
        if self.manifest_file.exists():
            self._registry.update(json.loads(self.manifest_file.read_text()))

    def save(self) -> None:
        self.manifest_file.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_file.write_text(json.dumps(self._registry, indent=2, ensure_ascii=False))

    @staticmethod
    def _generate_guid(path: Path) -> str:
        hasher = hashlib.md5()
        hasher.update(str(path).encode())
        return hasher.hexdigest()

    def import_resource(self, path: Path) -> str:
        """Добавить ресурс в манифест и вернуть его GUID."""
        path = Path(path)
        guid = self._generate_guid(path)
        self._registry[guid] = str(path)
        self.save()
        return guid

    def get_path(self, guid: str) -> Optional[Path]:
        path = self._registry.get(guid)
        return Path(path) if path else None

    def load(self, guid: str) -> Optional[bytes]:
        """Загрузить ресурс с диска или вернуть его из кэша."""
        if guid in self._cache:
            return self._cache[guid]
        path = self.get_path(guid)
        if path and path.exists():
            data = path.read_bytes()
            self._cache[guid] = data
            return data
        return None

    def search(self, keyword: str) -> Dict[str, Path]:
        """Поиск по имени файла в манифесте."""
        result: Dict[str, Path] = {}
        for guid, p in self._registry.items():
            if keyword.lower() in Path(p).name.lower():
                result[guid] = Path(p)
        return result
