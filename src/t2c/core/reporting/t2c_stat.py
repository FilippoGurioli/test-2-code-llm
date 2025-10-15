class RunStat:
    def __init__(
        self,
        code_gen_duration: float,
        is_code_gen_successful: bool,
        code_gen_error_message: str,
        test_validation_duration: float,
        number_of_tests: int,
        number_of_passed_tests: int,
        test_validation_errors: list[str],
        coverage: float,
    ) -> None:
        self.code_gen_duration = code_gen_duration
        self.is_code_gen_successful = is_code_gen_successful
        self.code_gen_error_message = code_gen_error_message
        self.test_validation_duration = test_validation_duration
        self.number_of_tests = number_of_tests
        self.number_of_passed_tests = number_of_passed_tests
        self.test_validation_errors = test_validation_errors
        self.coverage = coverage


class T2CStat:

    def __init__(
        self, model: str, language: str, attempts: int, runs: list[RunStat]
    ) -> None:
        self.model = model
        self.language = language
        self.attempts = attempts
        self.runs = runs
