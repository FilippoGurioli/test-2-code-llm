from t2c.core.reporting.observers.test_validation_observer import TestValidationObserver


class TestValidator:

    def __init__(self):
        self.observers = []

    def validate_tests(self, tests_path: str, src_path: str, command: str) -> bool:
        # TODO: Placeholder implementation
        return True

    def subscribe(self, observer: TestValidationObserver) -> None:
        self.observers.append(observer)

    def unsubscribe(self, observer: TestValidationObserver) -> None:
        self.observers.remove(observer)
