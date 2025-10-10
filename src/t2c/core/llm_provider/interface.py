from typing import Protocol


class LLMProviderInterface(Protocol):

    def generate_code(self, prompt: str) -> bool: ...
