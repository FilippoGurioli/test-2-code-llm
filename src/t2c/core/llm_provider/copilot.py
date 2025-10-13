from t2c.core.llm_provider.providers.remote_provider import RemoteProvider


class Copilot(RemoteProvider):

    def _get_server_model_name(self):
        return "todo"
