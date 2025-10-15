from t2c.core.reporting.code_gen_stats import CodeGenStat


class JsonCollector:

    def collect(self, data: CodeGenStat) -> None:
        print("Collecting data in JSON format")
