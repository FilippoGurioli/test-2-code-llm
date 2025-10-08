from t2c.cli.parsing.merged_config import MergedConfiguration


class PathValidator:
    """Validates if all paths present in the are valid (i.e. if the directory exists and is accessible)."""

    def validate(self, config: MergedConfiguration) -> None:
        paths: list[str] = []
        if config.command == "experiment":
            paths.append(config.config_path)
        else:
            paths.append(config.output_path, config.tests_path, config)
        self._check_validity_or_throw(paths)

    def _check_validity_or_throw(self, os_elem: list[str]) -> None:
        for _elem in os_elem:
            print("TODO")
