from t2c.core.llm_provider.interface import LLMProviderInterface
from t2c.core.llm_provider.supported_models import SupportedModels


class LLMProviderFactory:

    def create_provider(model: SupportedModels) -> LLMProviderInterface:
        match model:
            case SupportedModels.Smollm2:
                from t2c.core.llm_provider.providers.smollm2 import Smollm2

                return Smollm2()
            case SupportedModels.Qwen3:
                from t2c.core.llm_provider.providers.qwen3 import Qwen3

                return Qwen3()
            case SupportedModels.DeepSeek:
                from t2c.core.llm_provider.providers.deepseek import DeepSeek

                return DeepSeek()
            case SupportedModels.Mistral:
                from t2c.core.llm_provider.providers.mistral import Mistral

                return Mistral()
            case SupportedModels.Gemini:
                from t2c.core.llm_provider.gemini import Gemini

                return Gemini()
            case _:
                raise ValueError(f"Unknown LLM provider: {model}")
