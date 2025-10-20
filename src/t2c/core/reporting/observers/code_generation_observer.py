"""Module defining the CodeGenerationObserver protocol."""

from typing import Protocol


class CodeGenerationObserver(Protocol):
    """Interface for observing code generation events."""

    def on_code_generation_start(self) -> None:
        """Called when code generation starts."""
        ...

    def on_code_generation_end(
        self, chat: list[dict[str, str]], error: str | None
    ) -> None:
        """Called when code generation ends.

        Args:
            chat (list[dict[str, str]]): The chat history during code generation.
            error (str | None): Error message if code generation failed, None otherwise.
        """
        ...
