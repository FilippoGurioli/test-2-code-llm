from t2c.core.llm_provider.interface import LLMProviderInterface
from t2c.core.llm_provider.supported_models import SupportedModels


class LLMProviderFactory:

    def create_provider(model: SupportedModels) -> LLMProviderInterface:
        if model is SupportedModels.Smollm2:
            from t2c.core.llm_provider.providers.smollm2 import Smollm2

            return Smollm2()
        raise ValueError(f"Unknown LLM provider: {model}")
