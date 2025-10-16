import datetime
import shutil
from pathlib import Path

from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.core.code_generation_engine import CodeGenerationEngine
from t2c.core.llm_provider.llm_provider_factory import LLMProviderFactory
from t2c.core.llm_provider.supported_models import SupportedModels
from t2c.core.reporting.strategies.console_collector import ConsoleCollector
from t2c.core.reporting.strategies.json_collector import JsonCollector
from t2c.core.reporting_engine import ReportingEngine
from t2c.core.test_validation_engine import TestValidationEngine
from t2c.core.testing.runner_factory import RunnerFactory


class GenerateCommand:
    def get_help_text(self) -> str:
        return "This is the generate command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        self._clear_directory(config.output_path)
        attempts: int = 0
        cge, tve, reporting_engines = self._setup_engines(
            self._detect_test_kind(Path(config.tests_path)),  # TODO
            config.language,
            config.upper_bound,
            config.model,
            Path(config.output_path),
        )
        while attempts < config.upper_bound and (
            not cge.generate_code(config.tests_path, config.output_path)
            or not tve.validate_tests(config.tests_path, config.output_path)
        ):
            attempts += 1
        for re in reporting_engines:
            re.log_report()
        return None

    def _clear_directory(self, path: str) -> None:
        path: Path = Path(path)
        for item in path.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    def _setup_engines(
        self,
        test_kind: str,
        language: str,
        attempts: int,
        model: SupportedModels,
        output_path: Path,
    ) -> tuple[CodeGenerationEngine, TestValidationEngine, list[ReportingEngine]]:
        cge: CodeGenerationEngine = CodeGenerationEngine(
            LLMProviderFactory.create_provider(model)
        )
        tve: TestValidationEngine = TestValidationEngine(
            RunnerFactory.get_runner(language)
        )
        jre: ReportingEngine = ReportingEngine(
            id=test_kind
            + "-"
            + model.value
            + "-"
            + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            model=model.value,
            language=language,
            attempts=attempts,
            collect_strategy=JsonCollector(output_path / "report.json"),
        )
        cre: ReportingEngine = ReportingEngine(
            id=test_kind
            + "-"
            + model.value
            + "-"
            + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            model=model.value,
            language=language,
            attempts=attempts,
            collect_strategy=ConsoleCollector(),
        )
        cge.subscribe(jre)
        cge.subscribe(cre)
        tve.subscribe(jre)
        tve.subscribe(cre)
        return cge, tve, [jre, cre]

    def _detect_test_kind(self, tests_path: Path) -> str:
        if "unit" in tests_path.name.lower():
            return "UT"
        elif "integration" in tests_path.name.lower():
            return "IT"
        elif "acceptance" in tests_path.name.lower():
            return "AT"
        else:
            dirs = [p for p in tests_path.iterdir() if p.is_dir()]
            if len(dirs) == 1:
                return self._detect_test_kind(dirs[0])
            if len(dirs) == 0:
                return "Unknown"
            return "x".join(self._detect_test_kind(d) for d in dirs)
