"""Module defining the ValidationResult class used to represent validation outcomes."""


class ValidationResult:
    """Represents the result of a validation process."""

    def __init__(self, is_valid: bool, errors: list[str]):
        self.is_valid = is_valid
        self.errors = errors

    @staticmethod
    def success() -> "ValidationResult":
        """Creates a successful validation result.

        Returns:
            ValidationResult: A successful validation result.
        """
        return ValidationResult(True, [])

    @staticmethod
    def failure(errors: list[str] | str) -> "ValidationResult":
        """Creates a failed validation result.

        Args:
            errors (list[str] | str): The errors that caused the validation to fail.

        Returns:
            ValidationResult: A failed validation result.
        """
        if isinstance(errors, str):
            errors = [errors]
        return ValidationResult(False, errors)
