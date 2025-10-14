import os
import shlex
import subprocess

from t2c.core.reporting.observers.test_validation_observer import TestValidationObserver


class TestValidator:

    def __init__(self) -> None:
        self.observers: list[TestValidationObserver] = []

    def validate_tests(
        self, run_id: str, tests_path: str, src_path: str, command: str
    ) -> bool:
        """Run the project's tests and notify observers.

        By default this runs the `command` (e.g. 'pytest') locally in a subprocess
        with the working directory set to the repository root (where tests_path is
        relative to).

        Returns True if tests passed (exit code 0), False otherwise.
        """
        self._notify_start(run_id, tests_path)  # TODO
        cmd = shlex.split(command) + [tests_path]
        try:
            proc = subprocess.run(
                cmd,
                cwd=src_path or os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
                text=True,
            )
            output = proc.stdout or ""
            success = proc.returncode == 0
        except FileNotFoundError as exc:
            output = str(exc)
            success = False
        except Exception as exc:
            output = str(exc)
            success = False
        self._notify_end(not success)
        self._notify_metrics(1.0 if success else 0.0, 0)
        if not success:
            raise Exception(output) from None
        return success

    def subscribe(self, observer: TestValidationObserver) -> None:
        self.observers.append(observer)

    def unsubscribe(self, observer: TestValidationObserver) -> None:
        self.observers.remove(observer)

    def _notify_start(self, model_name: str, test_suite: str) -> None:
        for o in list(self.observers):
            o.on_test_validation_start(model_name, test_suite)

    def _notify_end(self, is_failed: bool) -> None:
        for o in list(self.observers):
            o.on_test_validation_end(is_failed)

    def _notify_metrics(self, test_pass_rate: float, coverage: float) -> None:
        for o in list(self.observers):
            o.on_test_metrics_measured(test_pass_rate, coverage)
