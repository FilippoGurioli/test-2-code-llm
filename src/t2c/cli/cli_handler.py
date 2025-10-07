from t2c.cli.parsing.argument_parser import ArgumentParser
from t2c.cli.parsing.config import Configuration


class CLIHandler:
    """Handles the command-line interface (CLI) of the application."""

    def parse_arguments(self, args: list[str]) -> Configuration:
        """Parses command-line arguments into a Configuration object.

        Args:
            args (List[str]): The command-line arguments to parse.

        Returns:
            Configuration: The parsed configuration object.
        """
        return ArgumentParser.parse(args)

    def validate_configuration(
        self, config: Configuration
    ):  # -> ValidatedConfiguration
        """Validates the given configuration.

        Args:
            config (Configuration): The configuration to validate.
        """
        pass  # Implementation of configuration validation would go here

    def execute_command(self, config):  # config: ValidatedConfiguration | -> None
        """Executes the command with the given configuration.

        Args:
            config (ValidatedConfiguration): The validated configuration to use.
        """
        pass  # Implementation of command execution would go here
