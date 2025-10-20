"""Module defining the interface for LLM providers."""

from typing import Protocol


class LLMProviderInterface(Protocol):
    """Interface for LLM providers."""

    def query(self, chat: list[dict[str, str]]) -> str:
        """Query the LLM model.

        Args:
            chat (list[dict[str, str]]): The chat history.

        Returns:
            str: The model's response.
        """
        ...
