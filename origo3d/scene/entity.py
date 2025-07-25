from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict
from pyrr import Vector3


@dataclass
class Entity:
    """Сущность сцены с идентификатором, именем, позицией и компонентами."""
    id: int
    name: str = ""
    position: Vector3 = field(default_factory=lambda: Vector3([0.0, 0.0, 0.0]))
    components: Dict[str, Any] = field(default_factory=dict)

    def add_component(self, key: str, component: Any) -> Any:
        """
        Добавить компонент под указанным ключом.
        Если у компонента есть атрибут `entity`, он будет автоматически установлен.
        """
        self.components[key] = component
        if hasattr(component, "entity"):
            setattr(component, "entity", self)
        return component

    def get_component(self, key: str) -> Any | None:
        """Получить компонент по ключу, либо `None`, если нет."""
        return self.components.get(key)

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать сущность в словарь.
        Позиция конвертируется в список из трёх чисел.
        """
        return {
            "id": self.id,
            "name": self.name,
            "position": list(self.position),  # [x, y, z]
            "components": {
                k: getattr(v, "to_dict", lambda: v)() for k, v in self.components.items()
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Entity:
        """
        Создать сущность из словаря.
        Ожидается, что `position` — это список из трёх чисел,
        а компоненты либо уже сконвертированы в нужные объекты, либо простые типы.
        """
        ent = cls(
            id=int(data["id"]),
            name=str(data.get("name", f"entity_{data['id']}")),
            position=Vector3(data.get("position", [0.0, 0.0, 0.0])),
            components={}  # заполним ниже
        )
        comps = data.get("components", {})
        for k, v in comps.items():
            # если нужно десериализовать сложные компоненты — 
            # здесь можно вставить логику построения через from_dict
            ent.components[k] = v
        return ent
