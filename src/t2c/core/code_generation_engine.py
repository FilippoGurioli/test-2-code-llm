from t2c.core.llm_provider.interface import LLMProviderInterface
from t2c.core.reporting.observers.code_generation_observer import CodeGenerationObserver


class CodeGenerationEngine:

    def __init__(self, llm_provider: LLMProviderInterface) -> None:
        self._llm_provider: LLMProviderInterface = llm_provider
        self._observers: list[CodeGenerationObserver] = []

    def subscribe(self, observer: CodeGenerationObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: CodeGenerationObserver) -> None:
        self._observers.remove(observer)

    def generate_code(self, tests_path: str, output_path: str) -> bool:
        return False  # TODO

    def _notify_start(self, model_name: str, test_suite: str) -> None:
        for obs in self._observers:
            obs.on_code_generation_start(model_name, test_suite)

    def _notify_end(self, is_failed: bool) -> None:
        for obs in self._observers:
            obs.on_code_generation_end(is_failed)
