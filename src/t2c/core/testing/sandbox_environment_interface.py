"""Module defining the SandboxEnvironmentInterface class."""

from pathlib import Path
from typing import Protocol


class SandboxEnvironment(Protocol):

    def setup(self) -> None:
        """Set up the sandbox environment."""
        ...

    def teardown(self) -> None:
        """Tear down the sandbox environment."""
        ...

    def run_command(self, command: list[str], cwd: Path) -> tuple[str, int]:
        """Run a command in the sandbox environment.

        Args:
            command (list[str]): The command to run.

        Returns:
            tuple[str, int]: A tuple containing the command output and exit code.
        """
        ...

    def copy_to_sandbox(self, local_path: Path, sandbox_path: Path) -> None:
        """Copy a file or directory to the sandbox environment.

        Args:
            local_path (Path): The local file or directory path.
            sandbox_path (Path): The destination path in the sandbox.
        """
        ...

    def delete_from_sandbox(self, sandbox_path: Path) -> None:
        """Delete a file or directory from the sandbox environment.

        Args:
            sandbox_path (Path): The file or directory path in the sandbox to delete.
        """
        ...

    def get_dirs(self, sandbox_path: Path) -> list[Path]:
        """Get a list of directories in the specified sandbox path.

        Args:
            sandbox_path (Path): The path in the sandbox to list directories from.

        Returns:
            list[Path]: A list of directory paths.
        """
        ...

    def get_files(self, sandbox_path: Path) -> list[Path]:
        """Get a list of files in the specified sandbox path.

        Args:
            sandbox_path (Path): The path in the sandbox to list files from.

        Returns:
            list[Path]: A list of file paths.
        """
        ...

    def touch(self, sandbox_path: Path) -> None:
        """Create an empty file at the specified sandbox path.

        Args:
            sandbox_path (Path): The file path in the sandbox to create.
        """
        ...
