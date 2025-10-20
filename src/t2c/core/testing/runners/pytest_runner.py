import os
import re
import subprocess
from pathlib import Path


class PytestRunner:

    def run(self, cwd: Path) -> tuple[int, int, float, str | None]:
        self._add_init_files(cwd)
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
            proc = subprocess.run(
                cmd,
                cwd=str(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
        except FileNotFoundError as exc:
            return (0, 0, 0.0, f"pytest not found: {exc}")
        output = proc.stdout or ""
        m = re.search(r"collected\s+(\d+)\s+items", output)
        if not m:
            m = re.search(r"collected\s+(\d+)", output)
        if m:
            try:
                total_tests = int(m.group(1))
            except Exception:
                total_tests = 0
        # Parse passed/failed/other summary counts from pytest output summary lines
        counts = {"passed": 0, "failed": 0, "skipped": 0, "xfailed": 0, "xpassed": 0}
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

        if proc.returncode != 0:
            # provide the last 800 chars of output as a diagnostic
            snippet = output.strip()[-800:]
            error_message = snippet or "pytest failed with non-zero exit code"

        return (passed_tests, total_tests, coverage, error_message)

    def _add_init_files(self, sandbox_path: Path) -> None:
        for dirpath, _, filenames in os.walk(sandbox_path):
            if "__init__.py" not in filenames:
                init_file = Path(dirpath) / "__init__.py"
                init_file.touch()
