"""Простейшее XOR-шифрование скриптов."""

from __future__ import annotations

from pathlib import Path


def encrypt(path: Path, key: bytes) -> bytes:
    """Возвращает содержимое файла, зашифрованное XOR-ключом.

    Параметры
    ----------
    path: :class:`Path`
        Путь до исходного файла.
    key: ``bytes``
        Последовательность байт, используемая для шифрования. Ключ
        повторяется по длине файла.
    """

    data = Path(path).read_bytes()
    if not key:
        raise ValueError("Key must not be empty")

    encrypted = bytearray(len(data))
    key_len = len(key)
    for i, b in enumerate(data):
        encrypted[i] = b ^ key[i % key_len]
    return bytes(encrypted)

