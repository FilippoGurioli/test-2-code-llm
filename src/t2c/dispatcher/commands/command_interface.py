from typing import Protocol

from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration


class Command(Protocol):
    """Command pattern for commands launched from cli."""

    def get_help_text(self) -> str: ...
    def execute(self, config: ValidatedConfiguration) -> None: ...
