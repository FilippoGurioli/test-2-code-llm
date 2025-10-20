"""Module responsible for validating the command in the configuration."""

from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validation_result import ValidationResult


class CommandValidator:
    """Checks if the command provided in the configuration is valid."""

    def validate(self, config: MergedConfiguration) -> ValidationResult:
        valid_commands = ["generate", "experiment"]
        errors: list[str] = []
        if config.command not in valid_commands:
            errors.append(
                f"Invalid command: {config.command}. Valid commands are: {', '.join(valid_commands)}."
            )
            return ValidationResult.failure(errors)
        return ValidationResult.success()
