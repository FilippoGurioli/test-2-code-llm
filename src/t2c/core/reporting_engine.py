import time

from t2c.core.reporting.collect_strategy import CollectStrategy
from t2c.core.reporting.t2c_stat import RunStat, T2CStat


class ReportingEngine:
    def __init__(
        self,
        run_id: str,
        model: str,
        language: str,
        attempts: str,
        collect_strategy: CollectStrategy,
    ) -> None:
        self._run_id = run_id
        self._model = model
        self._language = language
        self._attempts = attempts
        self._collect_strategy = collect_strategy
        self._runs: list[RunStat] = []

    def on_code_generation_start(self) -> None:
        self._code_gen_start_time = time.perf_counter()

    def on_code_generation_end(self, error: str | None = None) -> None:
        self._runs.append(
            RunStat(
                code_gen_duration=time.perf_counter() - self._code_gen_start_time,
                is_code_gen_successful=error is None,
                code_gen_error_message=error if error else "",
                test_validation_duration=0.0,
                number_of_tests=0,
                number_of_passed_tests=0,
                test_validation_errors=[],
                coverage=0.0,
            )
        )

    def on_test_validation_start(self) -> None:
        self._test_validation_start_time = time.perf_counter()

    def on_test_validation_end(self, errors: list[str] | None = None) -> None:
        self._runs[-1].test_validation_duration = (
            time.perf_counter() - self._test_validation_start_time
        )
        self._runs[-1].test_validation_errors = errors if errors else []

    def on_test_metrics_measured(
        self, num_tests: int, passed_tests: int, coverage: float
    ) -> None:
        self._runs[-1].number_of_tests = num_tests
        self._runs[-1].number_of_passed_tests = passed_tests
        self._runs[-1].coverage = coverage

    def log_report(self) -> None:
        self._collect_strategy.collect(
            T2CStat(
                model=self._model,
                language=self._language,
                attempts=self._attempts,
                runs=self._runs,
            )
        )
