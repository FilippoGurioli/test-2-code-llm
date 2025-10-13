from typing import Protocol


class LLMProviderInterface(Protocol):

    def query(self, prompt: str) -> str: ...
