from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Entity:
    """Простая сущность сцены."""

    id: int
    name: str
    components: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать сущность в словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "components": self.components,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entity":
        """Создать сущность из словаря."""
        return cls(
            id=int(data["id"]),
            name=str(data.get("name", f"entity_{data['id']}")),
            components=dict(data.get("components", {})),
        )
