from .config import Configuration


class ArgumentParser:
    """This class is responsible of parsing the argument provided as input from the user. It structures them into an object."""

    def parse(args: list[str]) -> Configuration:
        """Parses the given arguments.

        Args:
            args (list[str]): The arguments to parse.
        """
        config = Configuration()
        print("TODO: just assign all the config values here")
        return config
