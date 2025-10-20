"""Module defining the CollectStrategy interface for data collection strategies."""

from typing import Protocol

from t2c.core.reporting.t2c_stat import T2CStat


class CollectStrategy(Protocol):
    """Interface for data collection strategies."""

    def collect(self, data: T2CStat) -> None:
        """Collect data from the T2C process.

        Args:
            data (T2CStat): Data to be collected.
        """
        ...
