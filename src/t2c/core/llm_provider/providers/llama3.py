"""Module for Llama 3 model provider."""

from t2c.core.llm_provider.providers.local_provider import LocalProvider
from t2c.core.llm_provider.supported_models import SupportedModels


class Llama3(LocalProvider):
    """Llama 3 model provider class."""

    def _get_model(self) -> SupportedModels:
        return SupportedModels.Llama3
