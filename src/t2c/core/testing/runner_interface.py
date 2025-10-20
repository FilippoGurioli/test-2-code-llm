"""Module defining the interface for test runners."""

from pathlib import Path
from typing import Protocol

from t2c.core.testing.sandbox_environment_interface import SandboxEnvironment


class Runner(Protocol):

    def run(
        self, cwd: Path, environment: SandboxEnvironment
    ) -> tuple[int, int, float, str | None]:
        """Run the tests in the specified directory.

        Args:
            cwd (str): The directory where the tests should be run.
            environment (SandboxEnvironment): The sandbox environment to use for running the tests.

        Returns:
            tuple[int, int, float, str]: A tuple containing the following information:
                - The number of tests passed
                - The number of tests executed
                - The code coverage percentage
                - Any additional error messages
        """
        ...
