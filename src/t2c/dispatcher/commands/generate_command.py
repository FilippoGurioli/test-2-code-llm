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
        # TODO: add listeners to cge and ev
        while True:  # do-while like loop
            cge.generate_code(config.tests_path, config.output_path)
            attempts += 1
            if (
                tv.validate_tests(config.tests_path, config.output_path, config.command)
                or attempts >= config.upper_bound
            ):
                break
        return None
