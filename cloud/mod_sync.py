from __future__ import annotations

from pathlib import Path


def upload(local_path: Path, name: str) -> None:
    """Заглушка загрузки мода в облако."""
    print(f"Uploading {local_path} as {name} to cloud...")


def download(name: str, destination: Path) -> None:
    """Заглушка скачивания мода из облака."""
    destination.mkdir(parents=True, exist_ok=True)
    placeholder = destination / "placeholder.txt"
    placeholder.write_text(f"{name} downloaded from cloud")
    print(f"Downloaded {name} to {destination}")

