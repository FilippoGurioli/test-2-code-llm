from dataclasses import dataclass

from t2c.cli.parsing.config import Configuration


@dataclass(frozen=True)
class _Defaults:
    tests_path: str
    config_path: str | None
    output_path: str
    model_name: str
    upper_bound: int


class MergedConfiguration:
    """Holds the configuration merged with defaults and environment variables.

    All fields are set via the constructor and exposed as read-only
    properties. This prevents mutation after construction while keeping
    attribute-style access for callers.
    """

    def __init__(self, config: Configuration) -> None:
        self._command: str = (
            config.command
            if config.command is not None
            else (_ for _ in ()).throw(
                ValueError("'command' must be provided in the configuration")
            )
        )
        self._tests_path: str = (
            config.tests_path
            if config.tests_path is not None
            else self._get_default().tests_path
        )
        self._config_path: str | None = config.config_path
        self._output_path: str = (
            config.output_path
            if config.output_path is not None
            else self._get_default().output_path
        )
        self._model_name: str = (
            config.model_name
            if config.model_name is not None
            else self._get_default().model_name
        )
        self._upper_bound: int = (
            config.upper_bound
            if config.upper_bound is not None
            else self._get_default().upper_bound
        )

    @property
    def command(self) -> str:
        """The command to execute."""
        return self._command

    @property
    def tests_path(self) -> str:
        """Path to the tests directory or file."""
        return self._tests_path

    @property
    def config_path(self) -> str | None:
        """Path to the configuration file."""
        return self._config_path

    @property
    def output_path(self) -> str:
        """Path where generated code will be written."""
        return self._output_path

    @property
    def model_name(self) -> str:
        """Name of the model to use for code generation."""
        return self._model_name

    @property
    def upper_bound(self) -> int:
        """Upper bound for generation attempts."""
        return self._upper_bound

    def __str__(self) -> str:
        return (
            f"Configuration(command={self.command}, "
            f"testsPath={self.tests_path}, "
            f"configPath={self.config_path}, "
            f"outputPath={self.output_path}, "
            f"modelName={self.model_name}, "
            f"upperBound={self.upper_bound})"
        )

    def _get_default(self) -> _Defaults:
        return _Defaults(
            tests_path=".",
            config_path=None,
            output_path="./output",
            model_name="smollm2",
            upper_bound=3,
        )
