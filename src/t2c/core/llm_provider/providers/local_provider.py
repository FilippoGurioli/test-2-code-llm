"""Module for the Local LLM Provider using Ollama."""

import atexit
from abc import abstractmethod
from subprocess import DEVNULL, Popen, TimeoutExpired
from time import sleep

from requests import get

from t2c.core.llm_provider.providers.base_provider import BaseProvider
from t2c.core.llm_provider.supported_models import SupportedModels


class LocalProvider(BaseProvider):
    """Local LLM Provider using Ollama."""

    def __init__(self) -> None:
        self._ollama_process: Popen[bytes] | None = None
        super().__init__()

    def _clean_response(self, response: str) -> str:
        return self._remove_cot(response)

    def _remove_cot(self, response: str) -> str:
        """Removes chain-of-thought tags from the response."""
        start_cot_index = response.find("<think>")
        end_cot_index = response.find("</think>") + len("</think>")
        if start_cot_index == -1 or end_cot_index == -1:
            return response
        return response[:start_cot_index] + response[end_cot_index:]

    def _start_server(self) -> None:
        if not self._is_running():
            import os
            import shutil

            ollama_path = shutil.which("ollama")
            if not ollama_path:
                raise RuntimeError("Ollama binary not found. Install ollama.") from None

            try:
                self._ollama_process = Popen(
                    [ollama_path, "serve"],
                    stdout=DEVNULL,
                    stderr=DEVNULL,
                    close_fds=True,
                    env={"PATH": os.environ.get("PATH", "")},
                )  # nosec
            except FileNotFoundError:
                raise RuntimeError(
                    "Ollama is not executable at the provided path"
                ) from None
            atexit.register(self._stop_server)
            while not self._is_running():
                sleep(0.5)

    def _get_server_model_name(self) -> str:
        return f"ollama/{self._get_model().value.lower()}"

    def _stop_server(self) -> None:
        if self._ollama_process and self._ollama_process.poll() is None:
            self._ollama_process.terminate()
            try:
                self._ollama_process.wait(timeout=5)
            except TimeoutExpired:
                self._ollama_process.kill()

    def _is_running(self) -> bool:
        try:
            get(self._get_api_base(), timeout=1000)
            return True
        except Exception:
            return False

    def _get_api_base(self) -> str:
        return "http://localhost:11434"

    @abstractmethod
    def _get_model(self) -> SupportedModels:
        """Get the supported model for the provider.

        Returns:
            SupportedModels: The supported model.
        """
        pass
