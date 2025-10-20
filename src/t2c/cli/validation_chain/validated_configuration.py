"""Module defining the ValidatedConfiguration class representing a validated configuration."""

import datetime

import yaml

from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.core.llm_provider.supported_models import SupportedModels


class ValidatedConfiguration:
    """Data class that represent a valid configuration."""

    def __init__(self, config: MergedConfiguration, id: str | None = None) -> None:
        self.command: str = config.command
        if self.command == "experiment":
            self._parse_experiment_config(config)
        else:
            self.output_path = config.output_path
            self.model: SupportedModels = SupportedModels(config.model_name)
            self.tests_path: str = config.tests_path
            self.upper_bound = config.upper_bound
            self.language = config.language
            self.create_report: bool = config.create_report
            self.id: str = (
                id
                if id is not None
                else self.model.value
                + "-"
                + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            )

    def _parse_experiment_config(self, config: MergedConfiguration) -> None:
        result = yaml.safe_load(open(str(config.config_path)))
        if isinstance(result, dict):
            experiment_data: dict[str, str] = result.get("experiment", {})
            self.experiment_name: str = experiment_data.get("name", "experiment")
            self.output_path: str = experiment_data.get("output_dir", "./results")
            self.language: str = experiment_data.get("language", "python")
            self.upper_bound: int = int(experiment_data.get("upper_bound", "3"))
            raw_models: list[str] = result.get(
                "models", [m.value for m in list(SupportedModels)]
            )
            self.models: list[SupportedModels] = [
                SupportedModels(m) for m in raw_models
            ]
            self.tests_paths: list[tuple[str, str]] = [
                (test_kind["name"], test_kind["path"])
                for test_kind in result.get("test_kinds", [])
            ]
        else:
            raise ValueError(
                "The configuration file must contain a YAML dictionary at the top level."
            )
