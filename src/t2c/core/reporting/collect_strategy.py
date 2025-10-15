from typing import Protocol

from t2c.core.reporting.t2c_stat import T2CStat


class CollectStrategy(Protocol):
    def collect(self, data: T2CStat) -> None: ...
