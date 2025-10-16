import datetime

from t2c.cli.parsing.config import Configuration
from t2c.cli.parsing.merged_config import MergedConfiguration
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
        configs: list[ValidatedConfiguration] = []
        language: str = config.language
        upper_bound: int = config.upper_bound
        create_report: bool = True  # always true for experiments
        timestamp: str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        for model in config.models:
            for test_name, test_path in config.tests_paths:
                id: str = (
                    f"{config.experiment_name}-{model.value}-{test_name}-{timestamp}"
                )
                output_path: str = f"{config.output_path}/{config.experiment_name}"
                configs.append(
                    ValidatedConfiguration(
                        MergedConfiguration(
                            Configuration(
                                command="generate",
                                config_path=None,
                                language=language,
                                model_name=model.value,
                                upper_bound=upper_bound,
                                tests_path=test_path,
                                output_path=output_path,
                                create_report=create_report,
                            )
                        ),
                        id=id,
                    )
                )
        return configs
