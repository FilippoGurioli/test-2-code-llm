from t2c.cli.parsing.argument_parser import ArgumentParser
from t2c.cli.parsing.config import Configuration
from t2c.cli.parsing.configuration_merger import ConfigurationMerger


class CLIHandler:
    """Handles the command-line interface (CLI) of the application."""

    @staticmethod
    def parse_arguments(args: list[str]) -> Configuration:
        """Parses command-line arguments into a Configuration object.

        Args:
            args (List[str]): The command-line arguments to parse.

        Returns:
            Configuration: The parsed configuration object.
        """
        return ConfigurationMerger.merge(ArgumentParser.parse(args))

    @staticmethod
    def validate_configuration(
        config: Configuration,
    ) -> None:  # -> ValidatedConfiguration
        """Validates the given configuration.

        Args:
            config (Configuration): The configuration to validate.
        """
        pass  # Implementation of configuration validation would go here

    @staticmethod
    def execute_command(config) -> None:  # config: ValidatedConfiguration
        """Executes the command with the given configuration.

        Args:
            config (ValidatedConfiguration): The validated configuration to use.
        """
        pass  # Implementation of command execution would go here
