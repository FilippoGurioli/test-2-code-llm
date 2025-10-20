"""Module defining the TestValidationObserver protocol."""

from typing import Protocol


class TestValidationObserver(Protocol):
    """Interface for observing test validation events."""

    def on_test_validation_start(self) -> None:
        """Called when test validation starts."""
        ...

    def on_test_validation_end(self, error: str | None) -> None:
        """Called when test validation ends.

        Args:
            error (str | None): Error message if validation failed, None if successful.
        """
        ...

    def on_test_metrics_measured(
        self, num_tests: int, passed_tests: int, coverage: float
    ) -> None:
        """Called when test metrics are measured.

        Args:
            num_tests (int): Total number of tests.
            passed_tests (int): Number of tests that passed.
            coverage (float): Test coverage percentage.
        """
        ...
