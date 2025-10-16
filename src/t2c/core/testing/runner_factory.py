from t2c.core.testing.runner_interface import Runner
from t2c.core.testing.runners.pytest_runner import PytestRunner


class RunnerFactory:
    @staticmethod
    def get_runner(lang: str) -> Runner:
        """Factory method to get the appropriate Runner based on the programming language."""
        if lang == "python":
            return PytestRunner()
        else:
            raise ValueError(f"Unsupported language: {lang}")
