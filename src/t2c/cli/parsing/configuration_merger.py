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
        # parse upper bound from environment safely (don't call int on None)
        _upper_env = ConfigurationMerger._get_env_var_value("T2C_UPPER_BOUND")
        if _upper_env is not None:
            try:
                _upper_parsed: int | None = int(_upper_env)
            except ValueError:
                _upper_parsed = None
        else:
            _upper_parsed = None

        config_with_env_vars = Configuration(
            command=config.command,
            output_path=(
                config.output_path
                if config.output_path is not None
                else ConfigurationMerger._get_env_var_value("T2C_OUTPUT_DIR")
            ),
            config_path=(
                config.config_path
                if config.config_path is not None
                else ConfigurationMerger._get_env_var_value("T2C_CONFIG_FILE")
            ),
            tests_path=(
                config.tests_path
                if config.tests_path is not None
                else ConfigurationMerger._get_env_var_value("T2C_TESTS_DIR")
            ),
            model_name=(
                config.model_name
                if config.model_name is not None
                else ConfigurationMerger._get_env_var_value("T2C_MODEL_NAME")
            ),
            upper_bound=(
                config.upper_bound if config.upper_bound is not None else _upper_parsed
            ),
            language=(
                config.language
                if config.language is not None
                else ConfigurationMerger._get_env_var_value("T2C_LANGUAGE")
            ),
        )
        return MergedConfiguration(config_with_env_vars)

    @staticmethod
    def _get_env_var_value(var_name: str) -> str | None:
        raw = os.environ.get(var_name)
        if raw is None:
            return None
        value = raw.strip()
        if value == "":
            return None

        return value
