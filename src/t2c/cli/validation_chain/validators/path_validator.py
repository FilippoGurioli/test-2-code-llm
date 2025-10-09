import os
from pathlib import Path

from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validation_result import ValidationResult


class PathValidator:
    """Validates if all paths present in the configuration are valid (i.e. if the file/directory exists and is accessible)."""

    def validate(self, config: MergedConfiguration) -> ValidationResult:
        if config.command == "experiment" and config.config_path is None:
            return ValidationResult(
                False, ["For 'experiment' command, the config path must be provided."]
            )
        elif config.command == "experiment" and config.config_path is not None:
            path: Path = Path(str(config.config_path))
            if not path.exists():
                return ValidationResult(
                    False, [f"The config path '{config.config_path}' does not exist."]
                )
            if not path.is_file():
                return ValidationResult(
                    False, [f"The config path '{config.config_path}' is not a file."]
                )
            if not os.access(path, os.R_OK):
                return ValidationResult(
                    False, [f"The config path '{config.config_path}' is not readable."]
                )
        else:
            paths: list[Path] = [
                Path(str(config.tests_path)),
                Path(str(config.output_path)),
            ]
            for path in paths:
                if not path.exists():
                    return ValidationResult(
                        False, [f"The path '{path}' does not exist."]
                    )
                if not path.is_dir():
                    return ValidationResult(
                        False, [f"The path '{path}' is not a directory."]
                    )
                if not os.access(path, os.R_OK):
                    return ValidationResult(
                        False, [f"The path '{path}' is not readable."]
                    )
        return ValidationResult(True, [])
