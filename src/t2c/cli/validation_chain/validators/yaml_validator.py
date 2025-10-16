from pathlib import Path

import yaml

from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validation_result import ValidationResult


class YamlValidator:
    """Validates if the YAML configuration file is well-formed."""

    def validate(self, config: MergedConfiguration) -> ValidationResult:
        errors: list[str] = []
        if config.command.lower() != "experiment":
            return ValidationResult.success()
        if config.config_path is None:
            errors.append(
                "Configuration path must be provided for 'experiment' command."
            )
            return ValidationResult.failure(errors)
        configFile = Path(config.config_path)
        if not configFile.exists():
            errors.append(f"Configuration file does not exist: {config.config_path}")
            return ValidationResult.failure(errors)

        try:
            with open(config.config_path) as file:
                yaml.safe_load(file)
        except yaml.YAMLError as e:
            errors.append(f"YAML syntax error in configuration file: {e}")
            return ValidationResult.failure(errors)
        except Exception as e:
            errors.append(f"Error reading configuration file: {e}")
            return ValidationResult.failure(errors)
