"""Module defining the Validator interface for configuration validation."""

from typing import Protocol

from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validation_result import ValidationResult


class Validator(Protocol):
    """Generic validator that checks for config validity.

    Args:
        Protocol (Validator): interface for configuration validators.
    """

    def validate(self, config: MergedConfiguration) -> ValidationResult:
        """Validate the passed configuration.

        Args:
            config (MergedConfiguration): The configuration to validate.

        Returns:
            ValidationResult: The result of the validation.
        """
        ...
