from typing import Protocol


class LLMProviderInterface(Protocol):

    def query(self, chat: list[dict[str, str]]) -> str: ...
