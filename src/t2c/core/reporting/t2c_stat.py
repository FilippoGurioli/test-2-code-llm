class RunStat:
    def __init__(
        self,
        code_gen_duration: float,
        is_code_gen_successful: bool,
        test_validation_duration: float,
        number_of_tests: int,
        number_of_passed_tests: int,
        coverage: float,
    ) -> None:
        self.code_gen_duration = code_gen_duration
        self.is_code_gen_successful = is_code_gen_successful
        self.test_validation_duration = test_validation_duration
        self.number_of_tests = number_of_tests
        self.number_of_passed_tests = number_of_passed_tests
        self.coverage = coverage


class T2CStat:

    def __init__(
        self, model: str, language: str, attempts: int, runs: list[RunStat]
    ) -> None:
        self.model = model
        self.language = language
        self.attempts = attempts
        self.runs = runs
