import os
from pathlib import Path

from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validation_result import ValidationResult


class PathValidator:
    """Validates if all paths present in the configuration are valid (i.e. if the file/directory exists and is accessible)."""

    def validate(self, config: MergedConfiguration) -> ValidationResult:
        if config.command == "experiment" and config.config_path is None:
            return ValidationResult.failure(
                "For 'experiment' command, the config path must be provided."
            )
        elif config.command == "experiment" and config.config_path is not None:
            path: Path = Path(str(config.config_path))
            if not path.exists():
                return ValidationResult.failure(
                    f"The config path '{config.config_path}' does not exist."
                )
            if not path.is_file():
                return ValidationResult.failure(
                    f"The config path '{config.config_path}' is not a file."
                )
            if not os.access(path, os.R_OK):
                return ValidationResult.failure(
                    f"The config path '{config.config_path}' is not readable."
                )
        else:
            paths: list[Path] = [
                Path(str(config.tests_path)),
                Path(str(config.output_path)),
            ]
            is_valid: bool = True
            errors: list[str] = []
            for path in paths:
                if not path.exists():
                    errors.append(f"The path '{path}' does not exist.")
                    is_valid = False
                elif not path.is_dir():
                    errors.append(f"The path '{path}' is not a directory.")
                    is_valid = False
                elif not os.access(path, os.R_OK):
                    errors.append(f"The path '{path}' is not readable.")
                    is_valid = False
            if not is_valid:
                return ValidationResult.failure(errors)
        return ValidationResult.success()
