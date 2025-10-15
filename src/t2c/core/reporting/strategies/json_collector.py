import json

from t2c.core.reporting.t2c_stat import T2CStat


class JsonCollector:

    def __init__(self, output_path: str = "report.json") -> None:
        self._output_path = output_path

    def collect(self, data: T2CStat) -> None:
        print("Collecting data in JSON format")
        with open(self._output_path, "w") as f:
            json.dump(data, f)
