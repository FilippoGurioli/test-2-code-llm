"""Module for Smollm2 LLM provider."""

from t2c.core.llm_provider.providers.local_provider import LocalProvider
from t2c.core.llm_provider.supported_models import SupportedModels


class Smollm2(LocalProvider):
    """Smollm2 LLM provider class."""

    def _get_model(self) -> SupportedModels:
        return SupportedModels.Smollm2
