import argparse
import os
import subprocess
import sys
from pathlib import Path

# Импортируем runner из соседнего модуля
import scene_runner

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"


def list_assets() -> None:
    for root, _, files in os.walk(ASSETS_DIR):
        for file in files:
            rel = Path(root, file).relative_to(ASSETS_DIR)
            print(rel)


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI для управления Origo3D")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_p = subparsers.add_parser("run", help="Запустить сцену")
    run_p.add_argument("scene", help="Имя сцены")

    subparsers.add_parser("assets", help="Показать список ресурсов")

    build_p = subparsers.add_parser("build", help="Собрать игру")
    build_p.add_argument(
        "--platform",
        required=True,
        choices=["android", "ios", "wasm"],
        help="Целевая платформа",
    )

    args = parser.parse_args()

    if args.command == "run":
        scene_runner.run(args.scene)
    elif args.command == "assets":
        list_assets()
    elif args.command == "build":
        subprocess.run(
            [sys.executable, str(ROOT_DIR / "build" / "build_game.py"), "--platform", args.platform],
            check=True,
        )


if __name__ == "__main__":
    main()
