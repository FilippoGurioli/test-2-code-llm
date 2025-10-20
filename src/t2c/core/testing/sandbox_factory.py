"""Module defining the factory for sandbox environments."""

from t2c.core.testing.sandbox_environment_interface import SandboxEnvironment


class SandboxFactory:

    @staticmethod
    def local_env() -> SandboxEnvironment:
        """Create a local sandbox environment."""
        from t2c.core.testing.environments.local import LocalSandboxEnvironment

        return LocalSandboxEnvironment()

    # @staticmethod
    # def docker_env(image_name: str) -> SandboxEnvironment:
    #     """Create a Docker-based sandbox environment."""
    #     TODO
