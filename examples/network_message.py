"""Пример обмена сообщениями между клиентом и сервером."""

import argparse
import asyncio
from origo3d.networking import NetClient, NetServer


async def start_server(host: str, port: int) -> None:
    server = NetServer(host, port)
    await server.start()


async def start_client(name: str, host: str, port: int) -> None:
    client = NetClient(host, port)
    await client.connect()

    last: str | None = None

    async def display() -> None:
        nonlocal last
        while True:
            await asyncio.sleep(0.5)
            state = await client.replication.snapshot()
            msg = state.get(name, {}).get("msg")
            if msg and msg != last:
                print(f"{name} получил: {msg}")
                last = msg

    asyncio.create_task(display())

    try:
        while True:
            msg = input("Введите сообщение (пустая строка для выхода): ")
            if not msg:
                break
            await client.send_update({name: {"msg": msg}})
    finally:
        await client.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    server_p = subparsers.add_parser("server")
    client_p = subparsers.add_parser("client")
    client_p.add_argument("--name", default="user")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7777)
    args = parser.parse_args()

    if args.mode == "server":
        asyncio.run(start_server(args.host, args.port))
    else:
        asyncio.run(start_client(args.name, args.host, args.port))


if __name__ == "__main__":
    main()
