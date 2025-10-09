from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validation_result import ValidationResult
from t2c.cli.validation_chain.validator_interface import Validator


class ChainValidator:
    """Runs all validators over the passed configuration."""

    def __init__(self) -> None:
        self._validators: list[Validator] = []

    def add_validator(self, validator: Validator) -> None:
        """Adds a validator to the validators chain.

        Args:
            validator (Validator): The validator to add.
        """
        self._validators.append(validator)

    def validate(self, config: MergedConfiguration) -> ValidationResult:
        """Applies all validators to the given configuration.

        Args:
            config (MergedConfiguration): the configuration to validate.

        Returns:
            ValidationResult: The result of the validation.
        """
        errors: list[str] = []
        is_validation_succeeded: bool = True
        for validator in self._validators:
            result = validator.validate(config)
            is_validation_succeeded = is_validation_succeeded and result.is_valid
            errors.extend(result.errors)
        return ValidationResult(is_validation_succeeded, errors)
