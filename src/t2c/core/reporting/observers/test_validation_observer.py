from typing import Protocol


class TestValidationObserver(Protocol):
    def on_test_validation_start(self) -> None: ...

    def on_test_validation_end(self, errors: list[str] | None) -> None: ...

    def on_test_metrics_measured(
        self, num_tests: int, passed_tests: int, coverage: float
    ) -> None: ...
