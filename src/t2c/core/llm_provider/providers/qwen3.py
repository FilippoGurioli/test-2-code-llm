"""Module for Qwen3 LLM provider."""

from t2c.core.llm_provider.providers.local_provider import LocalProvider
from t2c.core.llm_provider.supported_models import SupportedModels


class Qwen3(LocalProvider):
    """Qwen3 LLM provider class."""

    def _get_model(self) -> SupportedModels:
        return SupportedModels.Qwen3
