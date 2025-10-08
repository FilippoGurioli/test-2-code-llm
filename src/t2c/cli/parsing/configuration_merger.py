from t2c.cli.parsing.config import Configuration


class ConfigurationMerger:
    """Merges Configuration objects with defaults and environment variables."""

    @staticmethod
    def merge(config: Configuration) -> Configuration:
        """Merges the given configuration with defaults and environment variables.

        Args:
            config (Configuration): The configuration to merge.

        Returns:
            Configuration: The merged configuration.
        """
        print("TODO")
        return config
