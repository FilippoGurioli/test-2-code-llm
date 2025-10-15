import shutil
from pathlib import Path

from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.core.code_generation_engine import CodeGenerationEngine
from t2c.core.llm_provider.llm_provider_factory import LLMProviderFactory
from t2c.core.test_validation_engine import TestValidationEngine


class GenerateCommand:
    def get_help_text(self) -> str:
        return "This is the generate command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        self._clear_directory(config.output_path)
        attempts: int = 0
        cge: CodeGenerationEngine = CodeGenerationEngine(
            LLMProviderFactory.create_provider(config.model)
        )
        tve: TestValidationEngine = TestValidationEngine()
        run_id: str = config.model + "-" + str(attempts)
        # TODO: add listeners to cge and tv
        self._dump_run(run_id)
        while True:  # do-while like loop
            if (
                attempts < config.upper_bound
                and not cge.generate_code(run_id, config.tests_path, config.output_path)
                or not tve.validate_tests(
                    run_id, config.tests_path, config.output_path, "pytest"
                )  # TODO
            ):
                attempts += 1
                run_id = config.model + "-" + str(attempts)
                self._dump_run(run_id)
            else:
                break
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
