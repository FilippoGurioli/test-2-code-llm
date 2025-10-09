from t2c.cli.parsing.argument_parser import ArgumentParser
from t2c.cli.parsing.configuration_merger import ConfigurationMerger
from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.chain_validator import ChainValidator
from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.dispatcher.command_factory import CommandFactory


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
        validation_result = self._chain_validator.validate(config)
        if not validation_result.is_valid:
            raise ValueError(
                "Configuration is not valid:\n" + "\n".join(validation_result.errors)
            )
        return ValidatedConfiguration(config)

    def execute_command(self, config: ValidatedConfiguration) -> None:
        """Executes the command with the given configuration.

        Args:
            config (ValidatedConfiguration): The validated configuration to use.

        Returns:
            None
        """
        # TODO: handle --help option with command.get_help_text()
        CommandFactory.get_command(config.command.value).execute(config)
