from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.dispatcher.command_factory import CommandFactory
from t2c.dispatcher.commands.command_interface import Command
from t2c.llm_provider.supported_models import SupportedModels


class ValidatedConfiguration:
    """Data class that represent a valid configuration."""

    def __init__(self, config: MergedConfiguration) -> None:
        self.command: Command = CommandFactory.get_command(config.command)
        if config.command == "experiment":
            self.config_path: str = str(config.config_path)
        else:
            self.output_path: str = config.output_path
            self.model: SupportedModels = SupportedModels(config.model_name)
            self.tests_path: str = config.tests_path
            self.upper_bound: int = config.upper_bound
