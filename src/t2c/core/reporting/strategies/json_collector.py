"""Module for collecting T2C statistics and appending them in JSON format."""

import json
from pathlib import Path

from t2c.core.reporting.t2c_stat import T2CStat


class JsonCollector:
    """Collector that appends T2C statistics to a JSON file."""

    def __init__(self, output_path: Path = Path("report.json")) -> None:
        self._output_path = output_path

    def collect(self, data: T2CStat) -> None:
        data_dict = data.to_dict()
        if self._output_path.exists() and self._output_path.stat().st_size > 0:
            try:
                with open(self._output_path, encoding="utf-8") as f:
                    existing_data = json.load(f)
                if not isinstance(existing_data, dict):
                    existing_data = {}
            except json.JSONDecodeError:
                existing_data = {}
        else:
            existing_data = {}

        existing_data.update(data_dict)

        with open(self._output_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2)
