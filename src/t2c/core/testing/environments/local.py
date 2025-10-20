"""Module defining a local sandbox environment."""

import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(tempfile.gettempdir()) / "t2c_sandbox"


class LocalSandboxEnvironment:
    """A local sandbox environment implementation."""

    def setup(self) -> None:
        pass  # Local environment does not require setup

    def teardown(self) -> None:
        pass  # Local environment does not require teardown

    def run_command(self, command: list[str], cwd: Path) -> tuple[str, int]:
        self._check_is_relative(cwd)
        absolute_cwd = BASE_DIR / cwd
        proc = subprocess.run(
            command,
            cwd=str(absolute_cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        output = proc.stdout or ""
        return output, proc.returncode

    def copy_to_sandbox(self, local_path: Path, sandbox_path: Path) -> None:
        self._check_is_relative(sandbox_path)
        absolute_sandbox_path = BASE_DIR / sandbox_path
        if local_path.is_dir():
            if not absolute_sandbox_path.exists():
                absolute_sandbox_path.mkdir(parents=True)
            for item in local_path.iterdir():
                self.copy_to_sandbox(item, sandbox_path / item.name)
        else:
            with local_path.open("rb") as src_file:
                with absolute_sandbox_path.open("wb") as dest_file:
                    dest_file.write(src_file.read())

    def delete_from_sandbox(self, sandbox_path: Path) -> None:
        self._check_is_relative(sandbox_path)
        absolute_sandbox_path = BASE_DIR / sandbox_path
        if absolute_sandbox_path.is_dir():
            for item in absolute_sandbox_path.iterdir():
                self.delete_from_sandbox(sandbox_path / item.name)
            absolute_sandbox_path.rmdir()
        else:
            absolute_sandbox_path.unlink()

    def get_dirs(self, sandbox_path: Path) -> list[Path]:
        self._check_is_relative(sandbox_path)
        absolute_sandbox_path = BASE_DIR / sandbox_path
        return [
            sandbox_path / p.name for p in absolute_sandbox_path.iterdir() if p.is_dir()
        ]

    def get_files(self, sandbox_path: Path) -> list[Path]:
        self._check_is_relative(sandbox_path)
        absolute_sandbox_path = BASE_DIR / sandbox_path
        return [
            sandbox_path / p.name
            for p in absolute_sandbox_path.iterdir()
            if p.is_file()
        ]

    def touch(self, sandbox_path: Path) -> None:
        self._check_is_relative(sandbox_path)
        absolute_sandbox_path = BASE_DIR / sandbox_path
        absolute_sandbox_path.parent.mkdir(parents=True, exist_ok=True)
        absolute_sandbox_path.touch()

    def _check_is_relative(self, path: Path) -> None:
        if path.is_absolute():
            raise ValueError("Path must be relative")
