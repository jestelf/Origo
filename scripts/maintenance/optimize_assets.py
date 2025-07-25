#!/usr/bin/env python3
"""Optimize images for mobile devices."""
from __future__ import annotations

from pathlib import Path
from PIL import Image


ROOT = Path("assets")


def optimize_image(file: Path) -> None:
    img = Image.open(file)
    img.thumbnail((512, 512))
    out = file.with_suffix(".webp")
    img.save(out, "WEBP", quality=80)
    print(f"Optimized {file} -> {out}")


def main() -> None:
    for ext in ("*.png", "*.jpg", "*.jpeg"):
        for path in ROOT.rglob(ext):
            optimize_image(path)


if __name__ == "__main__":
    main()
