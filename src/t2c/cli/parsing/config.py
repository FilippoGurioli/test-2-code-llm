class Configuration:
    """Holds the configuration of the application.

    All fields are set via the constructor and exposed as read-only
    properties. This prevents mutation after construction while keeping
    attribute-style access for callers.
    """

    def __init__(
        self,
        command: str | None,
        testsPath: str | None,
        configPath: str | None,
        outputPath: str | None,
        modelName: str | None,
        upperBound: int | None,
    ) -> None:
        self._command: str | None = command
        self._testsPath: str | None = testsPath
        self._configPath: str | None = configPath
        self._outputPath: str | None = outputPath
        self._modelName: str | None = modelName
        self._upperBound: int | None = upperBound

    @property
    def command(self) -> str | None:
        """The command to execute."""
        return self._command

    @property
    def testsPath(self) -> str | None:
        """Path to the tests directory or file."""
        return self._testsPath

    @property
    def configPath(self) -> str | None:
        """Path to the configuration file."""
        return self._configPath

    @property
    def outputPath(self) -> str | None:
        """Path where generated code will be written."""
        return self._outputPath

    @property
    def modelName(self) -> str | None:
        """Name of the model to use for code generation."""
        return self._modelName

    @property
    def upperBound(self) -> int | None:
        """Upper bound for generation attempts."""
        return self._upperBound

    def __str__(self) -> str:
        return (
            f"Configuration(command={self.command}, "
            f"testsPath={self.testsPath}, "
            f"configPath={self.configPath}, "
            f"outputPath={self.outputPath}, "
            f"modelName={self.modelName}, "
            f"upperBound={self.upperBound})"
        )
