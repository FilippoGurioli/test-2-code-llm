import importlib.util

from t2c.cli.parsing.merged_config import MergedConfiguration
from t2c.cli.validation_chain.validation_result import ValidationResult


class DependencyValidator:

    def validate(self, config: MergedConfiguration) -> ValidationResult:
        # For brevity I only check for python deps, it should be extended to support other languages
        required_dependencies = []
        if config.language == "python":
            required_dependencies = ["pytest", "pytest-cov"]
        missing_dependencies = []
        for dep in required_dependencies:
            if importlib.util.find_spec(dep) is None:
                missing_dependencies.append(dep)

        if missing_dependencies:
            return ValidationResult.failure(
                "Missing dependencies: " + ", ".join(missing_dependencies)
            )
        return ValidationResult.success()
