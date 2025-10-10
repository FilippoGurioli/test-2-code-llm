from typing import Protocol


class CodeGenerationObserver(Protocol):

    def on_code_generation_start(model_name: str, test_suite: str) -> None: ...

    def on_code_generation_end(is_failed: bool) -> None: ...
