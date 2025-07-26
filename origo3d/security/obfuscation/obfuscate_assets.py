"""Утилиты для упаковки и сжатия ресурсов."""

from __future__ import annotations

from pathlib import Path
import zipfile


def pack_assets(src_dir: Path, dest: Path) -> None:
    """Собрать все файлы из ``src_dir`` в zip-архив ``dest``.

    Файлы добавляются с относительными путями и сжимаются
    алгоритмом ``ZIP_DEFLATED``.
    """

    src = Path(src_dir)
    archive = Path(dest)
    archive.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in src.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(src))

