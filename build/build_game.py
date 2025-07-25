#!/usr/bin/env python3
"""Stub script to build Origo3D for various platforms."""
from __future__ import annotations

import argparse
from pathlib import Path


def build(platform: str) -> None:
    print(f"[build] Building for {platform}...")
    # Здесь могла бы быть логика сборки движка под нужную платформу
    # Для демонстрации просто создаём артефакт в каталоге build
    artifact = Path("build") / f"origo_{platform}.zip"
    artifact.touch()
    print(f"[build] Artifact created: {artifact}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Origo3D")
    parser.add_argument("--platform", required=True,
                        choices=["android", "ios", "wasm"],
                        help="Target platform")
    args = parser.parse_args()
    build(args.platform)


if __name__ == "__main__":
    main()
