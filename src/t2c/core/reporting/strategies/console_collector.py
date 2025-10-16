import json
import shutil
from enum import Enum

import yaml

from t2c.core.reporting.t2c_stat import T2CStat


class Format(Enum):
    JSON = "json"
    YAML = "yaml"
    CUSTOM = "custom"


class ConsoleCollector:

    def __init__(self, format: Format = Format.CUSTOM) -> None:
        self._format = format

    def collect(self, data: T2CStat) -> None:
        self._dump_delimiter()
        match self._format:
            case Format.JSON:
                self._dump_as_json(data)
            case Format.YAML:
                self._dump_as_yaml(data)
            case Format.CUSTOM:
                self._dump_as_custom(data)
        self._dump_delimiter()

    def _dump_delimiter(self, char: str = "=") -> None:
        columns = shutil.get_terminal_size((80, 20)).columns
        title = " T2C Report "
        print(char * columns)
        print(title.center(columns, char))
        print(char * columns)

    def _dump_as_json(self, data: T2CStat) -> None:
        print(json.dumps(data.to_dict(), indent=2))

    def _dump_as_yaml(self, data: T2CStat) -> None:
        print(yaml.dump(data.to_dict(), sort_keys=False))

    def _dump_as_custom(self, data: T2CStat) -> None:
        columns = shutil.get_terminal_size((80, 20)).columns
        print(f"ID: {data.id}")
        print(f"Model: {data.model}")
        print(f"Language: {data.language}")
        print(f"Attempts: {data.attempts}")
        print()

        for i, run in enumerate(data.runs, start=1):
            print(f" Run #{i} ".center(columns, "-"))
            print("Code Generation:")
            print(f"  - Duration: {run.code_gen_duration:.2f}s")
            print(f"  - Success: {'✅' if run.is_code_gen_successful else '❌'}")
            if run.code_gen_error_message:
                print(f"  - Error: {run.code_gen_error_message}")

            print("Test Validation:")
            print(f"  - Duration: {run.test_validation_duration:.2f}s")
            print(
                f"  - Tests Passed: {run.number_of_passed_tests}/{run.number_of_tests}"
            )
            print(f"  - Coverage: {run.coverage:.2f}%")

            if run.test_validation_error:
                print(f"  - Error: {run.test_validation_error}")
            print()

        print("-" * columns)
        avg_coverage = (
            sum(r.coverage for r in data.runs) / len(data.runs) if data.runs else 0.0
        )
        print(f"Average Coverage: {avg_coverage:.2f}%")
