class ValidationResult:
    """Represents the result of a validation process."""

    def __init__(self, is_valid: bool, errors: list[str]):
        self.is_valid = is_valid
        self.errors = errors

    @staticmethod
    def success():
        return ValidationResult(True, [])

    @staticmethod
    def failure(errors: list[str] | str):
        if isinstance(errors, str):
            errors = [errors]
        return ValidationResult(False, errors)
