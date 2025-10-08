from typing import Protocol

from t2c.cli.parsing.merged_config import MergedConfiguration


class Validator(Protocol):
    """Generic validator that checks for config validity.

    Args:
        Protocol (Validator): interface.
    """

    def validate(self, config: MergedConfiguration) -> None: ...
