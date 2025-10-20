"""Module for the TestValidationEngine class."""

import datetime
from pathlib import Path

from t2c.core.reporting.observers.test_validation_observer import TestValidationObserver
from t2c.core.testing.runner_interface import Runner
from t2c.core.testing.sandbox_environment_interface import SandboxEnvironment


class TestValidationEngine:
    """The TestValidationEngine is responsible for validating generated tests
    against the provided source code in an isolated sandbox environment."""

    def __init__(self, runner: Runner, sandbox: SandboxEnvironment) -> None:
        self.observers: list[TestValidationObserver] = []
        self._runner = runner
        self._sandbox = sandbox

    def validate_tests(self, tests_path: str, src_path: str) -> str | None:
        """Validate the generated tests against the provided source code.

        Args:
            tests_path (str): the path to the generated tests.
            src_path (str): the path to the source code.

        Returns:
            str | None: an error message if validation fails, otherwise None.
        """
        self._notify_start()
        self._sandbox.setup()
        sandbox_path = Path(datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ"))
        self._sandbox.copy_to_sandbox(
            Path(src_path), sandbox_path / Path(src_path).name
        )
        self._sandbox.copy_to_sandbox(
            Path(tests_path), sandbox_path / Path(tests_path).name
        )
        (passed_tests, total_tests, coverage, error_message) = self._runner.run(
            sandbox_path, self._sandbox
        )
        self._notify_end(error_message)
        self._notify_metrics(total_tests, passed_tests, coverage)
        self._sandbox.teardown()
        return error_message

    def subscribe(self, observer: TestValidationObserver) -> None:
        self.observers.append(observer)

    def unsubscribe(self, observer: TestValidationObserver) -> None:
        self.observers.remove(observer)

    def _notify_start(self) -> None:
        for o in list(self.observers):
            o.on_test_validation_start()

    def _notify_end(self, error: str | None) -> None:
        for o in list(self.observers):
            o.on_test_validation_end(error)

    def _notify_metrics(
        self, num_tests: int, passed_tests: int, coverage: float
    ) -> None:
        for o in list(self.observers):
            o.on_test_metrics_measured(num_tests, passed_tests, coverage)
