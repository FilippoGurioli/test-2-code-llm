from typing import TypeVar

from .config import Configuration

T = TypeVar("T")


class ArgumentParser:
    """This class is responsible of parsing the argument provided as input from the user. It structures them into an object."""

    @staticmethod
    def parse(args: list[str]) -> Configuration:
        """Parses the given arguments.

        Args:
            args (List[str]): The arguments to parse.
        """
        return Configuration(
            command=args[0] if len(args) > 0 else None,
            testsPath=ArgumentParser._extract_value_from_list(
                args, ("--testsPath", "-t"), str
            ),
            configPath=args[1] if len(args) > 1 else None,
            outputPath=ArgumentParser._extract_value_from_list(
                args, ("--outputPath", "-o"), str
            ),
            modelName=ArgumentParser._extract_value_from_list(
                args, ("--modelName", "-m"), str
            ),
            upperBound=ArgumentParser._extract_value_from_list(
                args, ("--upperBound", "-u"), int
            ),
        )

    @staticmethod
    def _extract_value_from_list(
        words: list[str], arg: tuple[str, str], t: type[T]
    ) -> T | None:
        """Extract and parse a value from a list of strings based on a key.

        Args:
            words (List[str]): The list of strings to search.
            arg (tuple[str, str]): The key to search for (long form, short form).
            t (Type[T]): The expected return type.

        Raises:
            ValueError: If multiple matching keys are found.
            ValueError: If the expected type cannot be parsed.

        Returns:
            Optional[T]: The extracted and parsed value, or None if not found.
        """

        matches = [s for s in words if arg[0] in s or arg[1] in s]

        if len(matches) == 0:
            return None
        elif len(matches) > 1:
            raise ValueError(f"Multiple matches found for '{arg}': {matches}")

        # Exactly one match
        match = matches[0]

        if "=" in match:
            value_str = match.split("=", 1)[1].strip()

        try:
            return t(value_str)
        except (ValueError, TypeError) as err:
            raise ValueError(f"Cannot convert '{value_str}' to {t.__name__}") from err
