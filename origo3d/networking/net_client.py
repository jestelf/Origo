from __future__ import annotations

"""Клиентская часть сетевого слоя."""

import asyncio
import json
import logging
from typing import Any, Dict

from .replication import ReplicationManager


class NetClient:
    """Базовый TCP-клиент для связи с :class:`NetServer`."""

    def __init__(self, host: str = "127.0.0.1", port: int = 7777) -> None:
        self.host = host
        self.port = port
        self.replication = ReplicationManager()
        self.logger = logging.getLogger(__name__)
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    async def connect(self) -> None:
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        self.logger.info("Соединение с сервером %s:%s", self.host, self.port)
        asyncio.create_task(self._listen())

    async def _listen(self) -> None:
        assert self._reader
        while True:
            data = await self._reader.readline()
            if not data:
                self.logger.info("Соединение закрыто сервером")
                break
            try:
                state: Dict[str, Dict[str, Any]] = json.loads(data.decode())
                await self.replication.merge_state(state)
            except json.JSONDecodeError:
                self.logger.warning("Получены некорректные данные: %s", data)

    async def send_update(self, update: Dict[str, Dict[str, Any]]) -> None:
        if not self._writer:
            return
        payload = (json.dumps(update) + "\n").encode()
        self._writer.write(payload)
        await self._writer.drain()

    async def close(self) -> None:
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
