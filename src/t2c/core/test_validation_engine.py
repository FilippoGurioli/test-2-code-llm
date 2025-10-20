import os
import tempfile
from pathlib import Path

from t2c.core.reporting.observers.test_validation_observer import TestValidationObserver
from t2c.core.testing.runner_interface import Runner

SANDBOX_BASE_DIR = Path(tempfile.gettempdir()) / "t2c_sandbox"


class TestValidationEngine:

    def __init__(self, runner: Runner) -> None:
        self.observers: list[TestValidationObserver] = []
        self._runner = runner

    def validate_tests(self, tests_path: str, src_path: str) -> bool:
        self._notify_start()
        sandbox_path = self._setup_sandbox()
        self._copy_dir_to_sandbox(tests_path, sandbox_path)
        self._copy_dir_to_sandbox(src_path, sandbox_path)
        (passed_tests, total_tests, coverage, error_message) = self._runner.run(
            sandbox_path
        )
        self._notify_end(error_message)
        self._notify_metrics(total_tests, passed_tests, coverage)
        return error_message is None

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

    def _copy_dir_to_sandbox(self, source_dir: str, sandbox_path: Path) -> None:
        import shutil

        for root, _, files in os.walk(source_dir):
            rel_root = os.path.relpath(root, source_dir)
            dest_root = sandbox_path / rel_root if rel_root != "." else sandbox_path
            dest_root.mkdir(parents=True, exist_ok=True)
            for file in files:
                if file.startswith(".") or file.endswith(".pyc"):
                    continue
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_root, file)
                shutil.copy2(src_file, dest_file)

    def _setup_sandbox(self) -> Path:
        import datetime

        if not SANDBOX_BASE_DIR.exists():
            SANDBOX_BASE_DIR.mkdir(parents=True, exist_ok=True)
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
        complete_path = SANDBOX_BASE_DIR / Path(date)
        complete_path.mkdir(parents=True, exist_ok=False)
        return complete_path
