from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration
from t2c.core.code_generation_engine import CodeGenerationEngine
from t2c.core.llm_provider_factory import LLMProviderFactory


class GenerateCommand:
    def get_help_text(self) -> str:
        return "This is the generate command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        cge: CodeGenerationEngine = CodeGenerationEngine(
            LLMProviderFactory.create_provider(config.model)
        )
        # TODO: add listeners to cge
        cge.generate_code(config.tests_path, config.output_path)
        return None
