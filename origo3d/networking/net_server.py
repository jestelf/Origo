from __future__ import annotations

"""Базовый сервер для сетевого режима."""

import asyncio
import json
import logging
from typing import Any, Dict, Set

from .replication import ReplicationManager


class NetServer:
    """Простейший TCP-сервер, синхронизирующий состояние объектов."""

    def __init__(self, host: str = "0.0.0.0", port: int = 7777) -> None:
        self.host = host
        self.port = port
        self.clients: Set[asyncio.StreamWriter] = set()
        self.replication = ReplicationManager()
        self.logger = logging.getLogger(__name__)

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        addr = writer.get_extra_info("peername")
        self.logger.info("Подключен клиент %s", addr)
        self.clients.add(writer)
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                try:
                    update: Dict[str, Dict[str, Any]] = json.loads(data.decode())
                    await self.replication.apply_update(update)
                    await self._broadcast()
                except json.JSONDecodeError:
                    self.logger.warning("Некорректные данные от %s: %s", addr, data)
        finally:
            self.logger.info("Клиент отключен %s", addr)
            self.clients.discard(writer)
            writer.close()
            await writer.wait_closed()

    async def _broadcast(self) -> None:
        state = await self.replication.snapshot()
        payload = (json.dumps(state) + "\n").encode()
        for client in list(self.clients):
            try:
                client.write(payload)
                await client.drain()
            except ConnectionError:
                self.clients.discard(client)

    async def start(self) -> None:
        server = await asyncio.start_server(self._handle_client, self.host, self.port)
        self.logger.info("Сервер слушает %s:%s", self.host, self.port)
        async with server:
            await server.serve_forever()
