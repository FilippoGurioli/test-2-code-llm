"""Module for the generate command."""

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
    """It launches a code generation and a test validation as many as configured upper bound."""

    def get_help_text(self) -> str:
        return "This is the generate command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        output_path = Path(config.output_path) / config.id
        output_path.mkdir(parents=True, exist_ok=True)
        attempts: int = 0
        cge, tve, reporting_engines = self._setup_engines(config)
        validation_error: str | None = None
        while True:  # do-while loop
            code_gen_succeeded = cge.generate_code(
                config.language,
                config.tests_path,
                output_path.__str__(),
                validation_error,
            )
            validation_error = tve.validate_tests(
                config.tests_path, output_path.__str__()
            )
            attempts += 1
            if (
                code_gen_succeeded and validation_error is None
            ) or attempts >= config.upper_bound:
                break
        for re in reporting_engines:
            re.log_report()
        return None

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
