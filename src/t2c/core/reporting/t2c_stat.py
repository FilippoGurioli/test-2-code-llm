"""Module for reporting T2C statistics."""

from typing import Any


class RunStat:
    """Statistics for a single run of the T2C process."""

    def __init__(
        self,
        code_gen_duration: float,
        is_code_gen_successful: bool,
        code_gen_error_message: str | None,
        test_validation_duration: float,
        number_of_tests: int,
        number_of_passed_tests: int,
        test_validation_error: str | None,
        coverage: float,
    ) -> None:
        self.code_gen_duration = code_gen_duration
        self.is_code_gen_successful = is_code_gen_successful
        self.code_gen_error_message = code_gen_error_message
        self.test_validation_duration = test_validation_duration
        self.number_of_tests = number_of_tests
        self.number_of_passed_tests = number_of_passed_tests
        self.test_validation_error = test_validation_error
        self.coverage = coverage

    def to_dict(self) -> dict[str, Any]:
        """Convert RunStat to a dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the RunStat.
        """
        return {
            "code-generation": {
                "time-taken": self.code_gen_duration,
                "success": self.is_code_gen_successful,
                "error": self.code_gen_error_message,
            },
            "test-validation": {
                "time-taken": self.test_validation_duration,
                "passed-tests": self.number_of_passed_tests,
                "number-of-tests": self.number_of_tests,
                "error": self.test_validation_error,
                "coverage": self.coverage,
            },
        }


class T2CStat:
    """Statistics for the T2C process."""

    def __init__(
        self, id: str, model: str, language: str, attempts: int, runs: list[RunStat]
    ) -> None:
        self.id = id
        self.model = model
        self.language = language
        self.attempts = attempts
        self.runs = runs

    def to_dict(self) -> dict[str, Any]:
        """Convert T2CStat to a dictionary representation.

        Returns:
            dict[str, Any]: Dictionary representation of the T2CStat.
        """
        return {
            self.id: {
                "model": self.model,
                "language": self.language,
                "attempts": self.attempts,
                "runs": [run.to_dict() for run in self.runs],
            }
        }
