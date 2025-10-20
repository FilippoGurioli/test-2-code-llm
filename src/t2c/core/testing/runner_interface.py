"""Module defining the interface for test runners."""

from pathlib import Path
from typing import Protocol


class Runner(Protocol):

    def run(self, cwd: Path) -> tuple[int, int, float, str | None]:
        """Run the tests in the specified directory.

        Args:
            cwd (str): The directory where the tests should be run.

        Returns:
            tuple[int, int, float, str]: A tuple containing the following information:
                - The number of tests passed
                - The number of tests executed
                - The code coverage percentage
                - Any additional error messages
        """
        ...
