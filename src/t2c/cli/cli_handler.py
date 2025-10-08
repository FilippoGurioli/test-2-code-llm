from t2c.cli.parsing.argument_parser import ArgumentParser
from t2c.cli.parsing.configuration_merger import ConfigurationMerger
from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.chain_validator import ChainValidator
from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration


class CLIHandler:
    """Handles the command-line interface (CLI) of the application."""

    def __init__(self, chain_validator: ChainValidator) -> None:
        self._chain_validator = chain_validator

    def parse_arguments(self, args: list[str]) -> MergedConfiguration:
        """Parses command-line arguments into a MergedConfiguration object.

        Args:
            args (list[str]): The command-line arguments to parse.

        Returns:
            MergedConfiguration: The parsed configuration object.
        """
        return ConfigurationMerger.merge(ArgumentParser.parse(args))

    def validate_configuration(
        self, config: MergedConfiguration
    ) -> ValidatedConfiguration:
        """Validates the given configuration.

        Args:
            config (MergedConfiguration): The configuration to validate.

        Returns:
            ValidatedConfiguration: The validated configuration.
        """
        return self._chain_validator.validate(config)

    def execute_command(self, config: MergedConfiguration) -> None:
        """Executes the command with the given configuration.

        Args:
            config (ValidatedConfiguration): The validated configuration to use.

        Returns:
            None
        """
        return None  # Implementation of command execution would go here
