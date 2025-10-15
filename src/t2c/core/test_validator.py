import os
import shlex
import subprocess
import tempfile
from pathlib import Path

from t2c.core.reporting.observers.test_validation_observer import TestValidationObserver

SANDBOX_BASE_DIR = Path(tempfile.gettempdir()) / "t2c_sandbox"


class TestValidator:

    def __init__(self) -> None:
        self.observers: list[TestValidationObserver] = []

    def validate_tests(
        self, run_id: str, tests_path: str, src_path: str, command: str
    ) -> bool:
        self._notify_start(run_id, tests_path)  # TODO
        sandbox_path = self._setup_sandbox(run_id)
        self._copy_dir_to_sandbox(tests_path, sandbox_path)
        self._copy_dir_to_sandbox(src_path, sandbox_path)
        self._add_init_files(sandbox_path)
        cmd = shlex.split(command)
        print("Running command:", " ".join(cmd))
        print("PWD:", sandbox_path)
        try:
            proc = subprocess.run(
                cmd,
                cwd=sandbox_path,
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
        print("TEST VALIDATION SUCEEDED!!!!")
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

    def _setup_sandbox(self, run_id: str) -> Path:
        import datetime

        model: Path = Path(run_id.split("-")[0])
        attempt: Path = Path(run_id.split("-")[1])
        if not SANDBOX_BASE_DIR.exists():
            SANDBOX_BASE_DIR.mkdir(parents=True, exist_ok=True)
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
        complete_path = SANDBOX_BASE_DIR / model / attempt / Path(date)
        complete_path.mkdir(parents=True, exist_ok=False)
        return complete_path

    def _add_init_files(self, sandbox_path: Path) -> None:
        for dirpath, _, filenames in os.walk(sandbox_path):
            if "__init__.py" not in filenames:
                init_file = Path(dirpath) / "__init__.py"
                init_file.touch()
