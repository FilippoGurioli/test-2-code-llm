from typing import TypeVar

T = TypeVar("T")


class ComponentLocator:

    def __init__(self) -> None:
        self._components: dict[str, T] = []

    def register(self, name: str, instance: T) -> None:
        if name in self._components:
            raise ValueError(f"Component with name '{name}' is already registered.")
        self._components[name] = instance

    def get(self, name: str) -> T:
        return self._components[name]
