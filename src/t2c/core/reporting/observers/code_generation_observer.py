from typing import Protocol


class CodeGenerationObserver(Protocol):

    def on_code_generation_start(self) -> None: ...

    def on_code_generation_end(self, error: str | None) -> None: ...
