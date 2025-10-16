import yaml

from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.core.llm_provider.supported_models import SupportedModels


class ValidatedConfiguration:
    """Data class that represent a valid configuration."""

    def __init__(self, config: MergedConfiguration) -> None:
        self.command: str = config.command
        if self.command == "experiment":
            result = yaml.safe_load(open(config.config_path))
            if isinstance(result, dict):
                self.experiment_name: str = result.get("name", "experiment")
                self.output_path: str = result.get("output_dir", "./results")
                self.language: str = result.get("language", "python")
                self.upper_bound: int = result.get("upper_bound", 3)
                raw_models: list[str] = result.get(
                    "models", [m.value() for m in list(SupportedModels)]
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
        else:
            self.output_path: str = config.output_path
            self.model: SupportedModels = SupportedModels(config.model_name)
            self.tests_path: str = config.tests_path
            self.upper_bound: int = config.upper_bound
            self.language: str = config.language
