from t2c.dispatcher.commands.command_interface import Command
from t2c.dispatcher.commands.experiment_command import ExperimentCommand
from t2c.dispatcher.commands.generate_command import GenerateCommand


class CommandFactory:
    """The factory pattern for commands."""

    @staticmethod
    def list_commands() -> list[str]:
        return ["generate", "experiment"]

    @staticmethod
    def get_command(name: str) -> Command:
        if name == "generate":
            return GenerateCommand()
        elif name == "experiment":
            return ExperimentCommand()
        else:
            raise ValueError(f"The command {name} does not exist")
