from t2c.core.llm_provider.providers.local_provider import LocalProvider
from t2c.core.llm_provider.supported_models import SupportedModels


class Llama3(LocalProvider):
    def _get_model(self) -> SupportedModels:
        return SupportedModels.Llama3
