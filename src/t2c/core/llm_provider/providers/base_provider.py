from abc import ABC, abstractmethod

from litellm import completion
from litellm.exceptions import APIConnectionError

REQUEST_TIMEOUT = 30000


class BaseProvider(ABC):
    def query(self, chat: list[dict[str, str]]) -> str:
        self._start_server()
        api_base = self._get_api_base()
        try:
            response = completion(
                model=self._get_server_model_name(),
                messages=chat,
                api_base=api_base,
                request_timeout=REQUEST_TIMEOUT,
            )
            cleaned_response = self._clean_response(response.choices[0].message.content)
            return cleaned_response
        except APIConnectionError as exc:
            raise RuntimeError(
                f"{self._get_server_model_name()} failed on API connection",
                REQUEST_TIMEOUT * 1000,
                str(exc),
                {"api_base": api_base},
            ) from exc

    @abstractmethod
    def _clean_response(self, response: str) -> str:
        pass

    @abstractmethod
    def _start_server(self) -> None:
        pass

    @abstractmethod
    def _get_server_model_name(self) -> str:
        pass

    @abstractmethod
    def _get_api_base(self) -> str:
        pass
