from t2c.cli.validation_chain.validated_configuration import ValidatedConfiguration


class GenerateCommand:
    def get_help_text(self) -> str:
        return "This is the generate command"  # TODO

    def execute(self, config: ValidatedConfiguration) -> None:
        print(self.get_help_text())
        return None
