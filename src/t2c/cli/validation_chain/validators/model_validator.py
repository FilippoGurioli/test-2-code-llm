from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validation_result import ValidationResult
from t2c.core.llm_provider.supported_models import SupportedModels


class ModelValidator:
    """Verifies if the specified LLM model is supported."""

    def validate(self, config: MergedConfiguration) -> ValidationResult:
        if config.model_name not in SupportedModels:
            return ValidationResult.failure(
                f"Model {config.model_name} is not supported."
            )
        return ValidationResult.success()
