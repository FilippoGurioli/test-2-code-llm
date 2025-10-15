from typing import property


class CodeGenStat:

    def __init__(
        self,
        model_name: str,
        test_suite: str,
        is_generation_succeeded: bool,
        is_validation_succeeded: bool,
        test_pass_rate: float,
        coverage: float,
        duration: float,
    ) -> None:
        self._model_name = model_name
        self._test_suite = test_suite
        self._is_generation_succeeded = is_generation_succeeded
        self._is_validation_succeeded = is_validation_succeeded
        self._test_pass_rate = test_pass_rate
        self._coverage = coverage
        self._duration = duration

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def test_suite(self) -> str:
        return self._test_suite

    @property
    def is_generation_succeeded(self) -> bool:
        return self._is_generation_succeeded

    @property
    def is_validation_succeeded(self) -> bool:
        return self._is_validation_succeeded

    @property
    def test_pass_rate(self) -> float:
        return self._test_pass_rate

    @property
    def coverage(self) -> float:
        return self._coverage

    @property
    def duration(self) -> float:
        return self._duration
