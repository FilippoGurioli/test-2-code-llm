from typing import Protocol

from t2c.core.reporting.code_gen_stats import CodeGenStat


class CollectStrategy(Protocol):
    def collect(self, data: CodeGenStat) -> None: ...
