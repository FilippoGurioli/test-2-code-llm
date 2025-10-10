from t2c.core.llm_provider.interface import LLMProviderInterface


class LLMProviderFactory:

    def create_provider(name: str) -> LLMProviderInterface:
        print("TODO")
