import argparse
import asyncio
import os
import subprocess
import sys
from pathlib import Path

# Импортируем runner из соседнего модуля
import scene_runner
from origo3d.networking import NetClient, NetServer

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"


def list_assets() -> None:
    for root, _, files in os.walk(ASSETS_DIR):
        for file in files:
            rel = Path(root, file).relative_to(ASSETS_DIR)
            print(rel)


def run_server(host: str, port: int) -> None:
    server = NetServer(host, port)
    asyncio.run(server.start())


async def _client_loop(host: str, port: int) -> None:
    client = NetClient(host, port)
    await client.connect()

    last_msg: str | None = None

    async def display() -> None:
        nonlocal last_msg
        while True:
            await asyncio.sleep(0.5)
            state = await client.replication.snapshot()
            msg = state.get("msg", {}).get("text")
            if msg and msg != last_msg:
                print(f"Получено: {msg}")
                last_msg = msg

    asyncio.create_task(display())

    try:
        while True:
            msg = input("Введите сообщение (пустая строка для выхода): ")
            if not msg:
                break
            await client.send_update({"msg": {"text": msg}})
    finally:
        await client.close()


def run_client(host: str, port: int) -> None:
    asyncio.run(_client_loop(host, port))


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

    server_p = subparsers.add_parser("server", help="Запустить сетевой сервер")
    server_p.add_argument("--host", default="0.0.0.0", help="Адрес сервера")
    server_p.add_argument("--port", type=int, default=7777, help="Порт сервера")

    client_p = subparsers.add_parser("client", help="Запустить сетевого клиента")
    client_p.add_argument("--host", default="127.0.0.1", help="Адрес сервера")
    client_p.add_argument("--port", type=int, default=7777, help="Порт сервера")

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
    elif args.command == "server":
        run_server(args.host, args.port)
    elif args.command == "client":
        run_client(args.host, args.port)


if __name__ == "__main__":
    main()
