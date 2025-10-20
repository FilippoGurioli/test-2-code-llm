"""Module for Remote LLM Provider."""

from t2c.core.llm_provider.providers.base_provider import BaseProvider


class RemoteProvider(BaseProvider):
    """Remote LLM Provider abstract class. It refers to LLM providers that exploit remote APIs."""

    def _clean_response(self, response: str) -> str:
        return response

    def _start_server(self) -> None:
        pass  # No server to start for remote provider
