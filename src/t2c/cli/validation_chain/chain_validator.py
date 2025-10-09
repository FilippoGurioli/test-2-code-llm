from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.cli.validation_chain.validator_interface import Validator


class ChainValidator:
    """Runs all validators over the passed configuration."""

    def __init__(self) -> None:
        self._validators: list[Validator] = []

    def add_validator(self, validator: Validator) -> None:
        self._validators.append(validator)

    def validate(self, config: MergedConfiguration) -> ValidatedConfiguration:
        errors: list[str] = []
        is_validation_succeeded: bool = True
        for validator in self._validators:
            result = validator.validate(config)
            is_validation_succeeded = is_validation_succeeded and result.is_valid
            errors.extend(result.errors)
        if not is_validation_succeeded:
            raise ValueError("Configuration is not valid:\n" + "\n".join(errors))
        return ValidatedConfiguration(config)
