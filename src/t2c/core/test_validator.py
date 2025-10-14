import shlex
import subprocess
from pathlib import Path

from t2c.core.reporting.observers.test_validation_observer import TestValidationObserver


class TestValidator:

    def __init__(self) -> None:
        self.observers: list[TestValidationObserver] = []

    def validate_tests(
        self, run_id: str, tests_path: str, src_path: str, command: str
    ) -> bool:
        self._notify_start(run_id, tests_path)  # TODO
        self._copy_test_to_src(tests_path, src_path)
        cmd = shlex.split(command) + [tests_path]
        print("Running command:", " ".join(cmd))
        print("PWD:", src_path or Path.cwd())
        try:
            proc = subprocess.run(
                cmd,
                cwd=src_path,
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

    def _copy_test_to_src(self, tests_path: str, src_path: str) -> None:
        import os
        import shutil

        if not os.path.isdir(tests_path):
            return
        for root, _, files in os.walk(tests_path):
            rel_root = os.path.relpath(root, tests_path)
            dest_root = (
                os.path.join(src_path, rel_root) if rel_root != "." else src_path
            )
            os.makedirs(dest_root, exist_ok=True)
            for file in files:
                if file.startswith("."):
                    continue
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_root, file)
                shutil.copy2(src_file, dest_file)
