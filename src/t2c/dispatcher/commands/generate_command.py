import shutil
from pathlib import Path

from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.core.code_generation_engine import CodeGenerationEngine
from t2c.core.llm_provider.llm_provider_factory import LLMProviderFactory
from t2c.core.reporting.strategies.console_collector import ConsoleCollector
from t2c.core.reporting.strategies.json_collector import JsonCollector
from t2c.core.reporting_engine import ReportingEngine
from t2c.core.test_validation_engine import TestValidationEngine
from t2c.core.testing.runner_factory import RunnerFactory


class GenerateCommand:
    def get_help_text(self) -> str:
        return "This is the generate command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        # self._clear_directory(config.output_path)
        output_path = Path(config.output_path) / config.id
        output_path.mkdir(parents=True, exist_ok=True)
        attempts: int = 0
        cge, tve, reporting_engines = self._setup_engines(config)
        while attempts < config.upper_bound and (
            not cge.generate_code(config.tests_path, output_path.__str__())
            or not tve.validate_tests(config.tests_path, output_path.__str__())
        ):
            attempts += 1
        for re in reporting_engines:
            re.log_report()
        return None

    def _clear_directory(self, path: str) -> None:
        p: Path = Path(path)
        for item in p.iterdir():
            if item.is_file() or item.is_symlink() and item.suffix == ".py":
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    def _setup_engines(
        self, config: ValidatedConfiguration
    ) -> tuple[CodeGenerationEngine, TestValidationEngine, list[ReportingEngine]]:
        cge: CodeGenerationEngine = CodeGenerationEngine(
            LLMProviderFactory.create_provider(config.model)
        )
        tve: TestValidationEngine = TestValidationEngine(
            RunnerFactory.get_runner(config.language)
        )
        cre: ReportingEngine = ReportingEngine(
            id=config.id,
            model=config.model.value,
            language=config.language,
            attempts=config.upper_bound,
            collect_strategy=ConsoleCollector(),
        )
        cge.subscribe(cre)
        tve.subscribe(cre)
        reporters = [cre]
        if config.create_report:
            jre: ReportingEngine = ReportingEngine(
                id=config.id,
                model=config.model.value,
                language=config.language,
                attempts=config.upper_bound,
                collect_strategy=JsonCollector(
                    Path(config.output_path) / "report.json"
                ),
            )
            cge.subscribe(jre)
            tve.subscribe(jre)
            reporters.append(jre)
        return cge, tve, reporters
