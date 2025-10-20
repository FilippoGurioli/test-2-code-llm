"""Module providing a factory to create appropriate test runners based on programming language."""

from t2c.core.testing.runner_interface import Runner
from t2c.core.testing.runners.pytest_runner import PytestRunner


class RunnerFactory:
    """Factory class to create test runners based on programming language."""

    @staticmethod
    def get_runner(lang: str) -> Runner:
        """Get the appropriate test runner for the specified programming language.

        Args:
            lang (str): The programming language for which to get the test runner.

        Raises:
            ValueError: If the specified language is not supported.

        Returns:
            Runner: The test runner for the specified programming language.
        """
        if lang == "python":
            return PytestRunner()
        else:
            raise ValueError(f"Unsupported language: {lang}")
