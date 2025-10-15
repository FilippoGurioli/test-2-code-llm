from t2c.core.reporting.collect_strategy import CollectStrategy


class ReportingEngine:
    def __init__(self, collect_strategy: CollectStrategy) -> None:
        self._collect_strategy = collect_strategy

    def on_code_generation_start(self, model_name: str, test_suite: str) -> None:
        print("code generation started")

    def on_code_generation_end(self, is_failed: bool) -> None:
        print("code generation ended")

    def on_test_validation_start(self, model_name: str, test_suite: str) -> None:
        print("test validation started")

    def on_test_validation_end(self, is_failed: bool) -> None:
        print("test validation ended")

    def on_test_metrics_measured(self, test_pass_rate: float, coverage: float) -> None:
        print("test metrics measured")
