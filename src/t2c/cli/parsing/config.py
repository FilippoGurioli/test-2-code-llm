class Configuration:
    """Holds the configuration of the application."""

    def __init__(
        self,
        testsPath: str,
        configPath: str,
        outputPath: str,
        modelName: str,
        upperBound: int,
    ):
        self.testsPath = testsPath
        self.configPath = configPath
        self.outputPath = outputPath
        self.modelName = modelName
        self.upperBound = upperBound
