from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.dispatcher.commands.generate_command import GenerateCommand


class ExperimentCommand:
    def get_help_text(self) -> str:
        return "This is the experiment command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        configs: list[ValidatedConfiguration] = self._compute_configuration_matrix(
            config
        )
        for cfg in configs:
            GenerateCommand().execute(cfg)
        return None

    def _compute_configuration_matrix(
        self, config: ValidatedConfiguration
    ) -> list[ValidatedConfiguration]:
        print("TODO")
