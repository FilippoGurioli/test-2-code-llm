"""Module for merging configuration with environment variables and defaults."""

import os

from t2c.cli.parsing.config import Configuration
from t2c.cli.parsing.merged_config import MergedConfiguration


class ConfigurationMerger:
    """Merges Configuration objects with defaults and environment variables."""

    @staticmethod
    def merge(config: Configuration) -> MergedConfiguration:
        """Merges the given configuration with defaults and environment variables.

        Args:
            config (Configuration): The configuration to merge.

        Returns:
            MergedConfiguration: The merged configuration.
        """
        config_with_env_vars = Configuration(
            command=config.command,
            output_path=(
                config.output_path
                if config.output_path is not None
                else ConfigurationMerger._parse_str_from_env("T2C_OUTPUT_DIR")
            ),
            config_path=(
                config.config_path
                if config.config_path is not None
                else ConfigurationMerger._parse_str_from_env("T2C_CONFIG_FILE")
            ),
            tests_path=(
                config.tests_path
                if config.tests_path is not None
                else ConfigurationMerger._parse_str_from_env("T2C_TESTS_DIR")
            ),
            model_name=(
                config.model_name
                if config.model_name is not None
                else ConfigurationMerger._parse_str_from_env("T2C_MODEL_NAME")
            ),
            upper_bound=(
                config.upper_bound
                if config.upper_bound is not None
                else ConfigurationMerger._parse_int_from_env("T2C_UPPER_BOUND")
            ),
            language=(
                config.language
                if config.language is not None
                else ConfigurationMerger._parse_str_from_env("T2C_LANGUAGE")
            ),
            create_report=(
                config.create_report
                if config.create_report is not None
                else ConfigurationMerger._parse_bool_from_env("T2C_CREATE_REPORT")
            ),
        )
        return MergedConfiguration(config_with_env_vars)

    @staticmethod
    def _parse_int_from_env(var_name: str) -> int | None:
        env = os.environ.get(var_name)
        if env is not None:
            try:
                parsed: int | None = int(env)
            except ValueError:
                parsed = None
        else:
            parsed = None
        return parsed

    @staticmethod
    def _parse_bool_from_env(var_name: str) -> bool | None:
        raw = os.environ.get(var_name)
        if raw is None:
            return None
        value = raw.strip().lower()
        if value in ("true", "1", "yes"):
            return True
        elif value in ("false", "0", "no"):
            return False
        else:
            return None

    @staticmethod
    def _parse_str_from_env(var_name: str) -> str | None:
        raw = os.environ.get(var_name)
        if raw is None:
            return None
        value = raw.strip()
        if value == "":
            return None

        return value
