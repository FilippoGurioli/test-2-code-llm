class Configuration:
    """Holds the configuration of the application.

    All fields are set via the constructor and exposed as read-only
    properties. This prevents mutation after construction while keeping
    attribute-style access for callers.
    """

    def __init__(
        self,
        command: str | None,
        tests_path: str | None,
        config_path: str | None,
        output_path: str | None,
        model_name: str | None,
        upper_bound: int | None,
    ) -> None:
        self._command: str | None = command
        self._tests_path: str | None = tests_path
        self._config_path: str | None = config_path
        self._output_path: str | None = output_path
        self._model_name: str | None = model_name
        self._upper_bound: int | None = upper_bound

    @property
    def command(self) -> str | None:
        """The command to execute."""
        return self._command

    @property
    def tests_path(self) -> str | None:
        """Path to the tests directory or file."""
        return self._tests_path

    @property
    def config_path(self) -> str | None:
        """Path to the configuration file."""
        return self._config_path

    @property
    def output_path(self) -> str | None:
        """Path where generated code will be written."""
        return self._output_path

    @property
    def model_name(self) -> str | None:
        """Name of the model to use for code generation."""
        return self._model_name

    @property
    def upper_bound(self) -> int | None:
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
