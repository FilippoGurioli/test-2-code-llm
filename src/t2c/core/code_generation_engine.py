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
        self._notify_start(self._llm_provider.__class__.__str__, "pytest")  # TODO
        result: bool = self._llm_provider.generate_code(
            f"This is an example prompt that uses {tests_path} and {output_path}"
        )
        self._notify_end(result)
        return result

    def _notify_start(self, model_name: str, test_suite: str) -> None:
        for obs in self._observers:
            obs.on_code_generation_start(model_name, test_suite)

    def _notify_end(self, is_failed: bool) -> None:
        for obs in self._observers:
            obs.on_code_generation_end(is_failed)
