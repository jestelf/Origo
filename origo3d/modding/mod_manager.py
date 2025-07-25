from __future__ import annotations

from pathlib import Path
from typing import List

from cloud import mod_sync


class ModManager:
    """Простое управление локальными модами."""

    def __init__(self, mods_dir: Path | str = "user_content/mods") -> None:
        self.mods_dir = Path(mods_dir)
        self.mods_dir.mkdir(parents=True, exist_ok=True)

    def list_installed(self) -> List[str]:
        """Вернуть список установленных модов."""
        return [p.name for p in self.mods_dir.iterdir() if p.is_dir()]

    def install_from_cloud(self, mod_name: str) -> None:
        """Скачать мод из облака."""
        dest = self.mods_dir / mod_name
        dest.mkdir(exist_ok=True)
        mod_sync.download(mod_name, dest)

    def upload_to_cloud(self, mod_name: str) -> None:
        """Загрузить мод в облако."""
        path = self.mods_dir / mod_name
        if path.exists():
            mod_sync.upload(path, mod_name)

    def remove_mod(self, mod_name: str) -> None:
        """Удалить мод локально."""
        path = self.mods_dir / mod_name
        if path.is_dir():
            for item in path.iterdir():
                if item.is_file():
                    item.unlink()
                else:
                    for sub in item.rglob('*'):
                        if sub.is_file():
                            sub.unlink()
                    for sub in sorted(item.rglob('*'), reverse=True):
                        if sub.is_dir():
                            sub.rmdir()
            path.rmdir()

