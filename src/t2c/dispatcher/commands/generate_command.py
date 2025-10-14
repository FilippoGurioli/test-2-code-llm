from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.core.code_generation_engine import CodeGenerationEngine
from t2c.core.llm_provider_factory import LLMProviderFactory
from t2c.core.test_validator import TestValidator


class GenerateCommand:
    def get_help_text(self) -> str:
        return "This is the generate command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        attempts: int = 0
        cge: CodeGenerationEngine = CodeGenerationEngine(
            LLMProviderFactory.create_provider(config.model)
        )
        tv: TestValidator = TestValidator()
        run_id: str = config.model + "-" + str(attempts)
        # TODO: add listeners to cge and tv
        while True:  # do-while like loop
            if (
                attempts < config.upper_bound
                and not cge.generate_code(run_id, config.tests_path, config.output_path)
                or not tv.validate_tests(
                    run_id, config.tests_path, config.output_path, "pytest"
                )  # TODO
            ):
                attempts += 1
                run_id = config.model + "-" + str(attempts)
            else:
                break
        return None
