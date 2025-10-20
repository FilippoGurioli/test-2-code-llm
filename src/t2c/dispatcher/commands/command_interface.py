"""Module for the command interface."""

from typing import Protocol

from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration


class Command(Protocol):
    """Command pattern for commands launched from cli."""

    def get_help_text(self) -> str:
        """Returns the help text to display on terminal.

        Returns:
            str: The help text.
        """
        ...

    def execute(self, config: ValidatedConfiguration) -> None:
        """Executes the command with the passed configuration.

        Args:
            config (ValidatedConfiguration): The validated configuration to use.
        """
        ...
