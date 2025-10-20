"""Module implementing a test runner using pytest."""

import re
from pathlib import Path

from t2c.core.testing.sandbox_environment_interface import SandboxEnvironment


class PytestRunner:
    """It runs pytest."""

    def run(
        self, cwd: Path, sandbox: SandboxEnvironment
    ) -> tuple[int, int, float, str | None]:
        self._delete_pycache(cwd, sandbox)
        self._add_init_files(cwd, sandbox)
        passed_tests = 0
        total_tests = 0
        coverage = 0.0
        error_message: str | None = None
        cmd = [
            "pytest",
            "--disable-warnings",
            "--maxfail=1",
            "--cov=.",
            "--cov-report=term",
        ]
        try:
            stdout, returncode = sandbox.run_command(cmd, cwd)
        except FileNotFoundError as exc:
            return (0, 0, 0.0, f"pytest not found: {exc}")
        output = stdout or ""
        total_tests = self._get_total_tests(output)
        passed_tests, total_tests = self._get_passed_tests(output, total_tests)
        coverage = self._get_coverage(output)
        if returncode != 0:
            # provide the last 800 chars of output as a diagnostic
            snippet = output.strip()[-800:]
            error_message = snippet or "pytest failed with non-zero exit code"
        return (passed_tests, total_tests, coverage, error_message)

    def _add_init_files(self, sandbox_path: Path, sandbox: SandboxEnvironment) -> None:
        sandbox.touch(sandbox_path / "__init__.py")
        for dir in sandbox.get_dirs(sandbox_path):
            self._add_init_files(dir, sandbox)

    def _delete_pycache(self, sandbox_path: Path, sandbox: SandboxEnvironment) -> None:
        for dir in sandbox.get_dirs(sandbox_path):
            if dir.name == "__pycache__":
                sandbox.delete_from_sandbox(dir)
            else:
                self._delete_pycache(dir, sandbox)

    def _get_total_tests(self, output: str) -> int:
        m = re.search(r"collected\s+(\d+)\s+items", output)
        if not m:
            m = re.search(r"collected\s+(\d+)", output)
        if m:
            try:
                total_tests = int(m.group(1))
            except Exception:
                total_tests = 0
        return total_tests if m else 0

    def _get_passed_tests(self, output: str, total_tests: int) -> tuple[int, int]:
        counts = {"passed": 0, "failed": 0, "skipped": 0, "xfailed": 0, "xpassed": 0}
        passed_tests = 0
        for key in counts.keys():
            mm = re.search(rf"(\d+)\s+{key}", output)
            if mm:
                try:
                    counts[key] = int(mm.group(1))
                except Exception:
                    counts[key] = 0

        if counts["passed"]:
            passed_tests = counts["passed"]
        elif (
            total_tests
            and counts["failed"]
            + counts["skipped"]
            + counts["xfailed"]
            + counts["xpassed"]
            >= 0
        ):
            passed_tests = max(0, total_tests - counts["failed"] - counts["skipped"])
        if not total_tests:
            total_tests = (
                counts["passed"]
                + counts["failed"]
                + counts["skipped"]
                + counts["xfailed"]
                + counts["xpassed"]
            )
        return (passed_tests, total_tests)

    def _get_coverage(self, output: str) -> float:
        cov_m = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)
        if cov_m:
            try:
                coverage = float(cov_m.group(1))
            except Exception:
                coverage = 0.0
        else:
            cov_m2 = re.search(r"TOTAL\s+.*?(\d+)%", output)
            if cov_m2:
                try:
                    coverage = float(cov_m2.group(1))
                except Exception:
                    coverage = 0.0
        return coverage if cov_m or cov_m2 else 0.0
