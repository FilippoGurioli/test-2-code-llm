import atexit
from subprocess import DEVNULL, Popen, TimeoutExpired
from time import sleep

from litellm import completion
from litellm.exceptions import APIConnectionError
from requests import get

from t2c.core.llm_provider.supported_models import SupportedModels

REQUEST_TIMEOUT = 300  # seconds


class Smollm2:
    def query(self, prompt: str) -> str:
        self._start_server(SupportedModels.Smollm2)
        _chat_history: list[dict[str, str]] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        _chat_history.append({"content": prompt, "role": "user"})
        api_base = self._get_api_base(SupportedModels.Smollm2)
        try:
            response = completion(
                model=self._get_server_model_name(SupportedModels.Smollm2),
                messages=_chat_history,
                api_base=api_base,
                request_timeout=REQUEST_TIMEOUT,
            )
            _chat_history.append({"content": response, "role": "assistant"})
            cleaned_response = self._clean_response(response.choices[0].message.content)
            return cleaned_response
        except APIConnectionError as exc:
            raise RuntimeError(
                "smollm2 failed on API connection",
                REQUEST_TIMEOUT * 1000,
                str(exc),
                {"api_base": api_base},
            ) from exc

    def _clean_response(self, response: str) -> str:
        return self._remove_cot(self._remove_quotes(response))

    def _remove_quotes(self, response: str) -> str:
        return response.replace("```", "").strip()

    def _remove_cot(self, response: str) -> str:
        start_cot_index = response.find("<think>")
        end_cot_index = response.find("</think>") + len("</think>")
        if start_cot_index == -1 or end_cot_index == -1:
            return response
        return response[:start_cot_index] + response[end_cot_index:]

    def _start_server(self, supported_model: SupportedModels) -> None:
        if (
            supported_model != SupportedModels.Copilot
            and supported_model != SupportedModels.Gemini
        ):
            if not self._is_running():
                import os
                import shutil

                ollama_path = shutil.which("ollama")
                if not ollama_path:
                    raise RuntimeError(
                        "Ollama binary not found. Install ollama."
                    ) from None

                global ollama_process
                try:
                    ollama_process = Popen(
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

                # wait for health endpoint
                while not self._is_running():
                    sleep(0.5)

    def _get_server_model_name(self, supported_model: SupportedModels) -> str:
        if supported_model == SupportedModels.Copilot:
            print("TODO")
        elif supported_model == SupportedModels.Gemini:
            print("TODO")
        else:
            return f"ollama/{supported_model.value.lower()}"

    def _stop_server(self):
        global ollama_process
        if ollama_process and ollama_process.poll() is None:
            ollama_process.terminate()
            try:
                ollama_process.wait(timeout=5)
            except TimeoutExpired:
                ollama_process.kill()

    def _is_running(self) -> bool:
        try:
            get("http://localhost:11434", timeout=1000)
            return True
        except Exception:
            return False

    def _get_api_base(self, supported_model: SupportedModels) -> str:
        if supported_model == SupportedModels.Copilot:
            print("TODO")
        elif supported_model == SupportedModels.Gemini:
            print("TODO")
        else:
            return "http://localhost:11434"
