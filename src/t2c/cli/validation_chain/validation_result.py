class ValidationResult:
    """Represents the result of a validation process."""

    def __init__(self, is_valid: bool, errors: list[str]):
        self.is_valid = is_valid
        self.errors = errors
