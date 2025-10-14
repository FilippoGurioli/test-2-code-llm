from t2c.core.llm_provider.providers.base_provider import BaseProvider


class RemoteProvider(BaseProvider):
    def _clean_response(self, response: str) -> str:
        return response

    def _start_server(self) -> None:
        pass  # No server to start for remote provider
