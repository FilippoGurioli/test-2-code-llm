"""Module for DeepSeek LLM provider."""

from t2c.core.llm_provider.providers.local_provider import LocalProvider
from t2c.core.llm_provider.supported_models import SupportedModels


class DeepSeek(LocalProvider):
    """DeepSeek LLM provider implementation."""

    def _get_model(self) -> SupportedModels:
        return SupportedModels.DeepSeek
