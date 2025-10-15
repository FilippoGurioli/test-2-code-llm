import shutil
from pathlib import Path

from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.core.code_generation_engine import CodeGenerationEngine
from t2c.core.llm_provider.llm_provider_factory import LLMProviderFactory
from t2c.core.llm_provider.supported_models import SupportedModels
from t2c.core.reporting.strategies.json_collector import JsonCollector
from t2c.core.reporting_engine import ReportingEngine
from t2c.core.test_validation_engine import TestValidationEngine


class GenerateCommand:
    def get_help_text(self) -> str:
        return "This is the generate command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        self._clear_directory(config.output_path)
        attempts: int = 0
        cge, tve = self._setup_engines(config.model)
        run_id: str = config.model + "-" + str(attempts)
        self._dump_run(run_id)
        while (
            attempts < config.upper_bound
            and not cge.generate_code(run_id, config.tests_path, config.output_path)
            or not tve.validate_tests(
                run_id,
                config.tests_path,
                config.output_path,
                "pytest",  # TODO make configurable
            )
        ):
            attempts += 1
            run_id = config.model + "-" + str(attempts)
            self._dump_run(run_id)
        return None

    def _dump_run(self, run_id: str) -> None:
        print("==================================")
        print(" Starting run:", run_id)
        print("==================================")

    def _clear_directory(self, path: str) -> None:
        path: Path = Path(path)
        for item in path.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    def _setup_engines(
        self, model: SupportedModels
    ) -> tuple[CodeGenerationEngine, TestValidationEngine]:
        cge: CodeGenerationEngine = CodeGenerationEngine(
            LLMProviderFactory.create_provider(model)
        )
        tve: TestValidationEngine = TestValidationEngine()
        re: ReportingEngine = ReportingEngine(JsonCollector())
        cge.subscribe(re)
        tve.subscribe(re)
        return cge, tve
