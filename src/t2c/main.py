import sys

from t2c.cli.cli_handler import CLIHandler


def main(args: list[str] | None = None) -> int:
    """Main entry point."""
    if args is None:
        args = sys.argv[1:]

    print(CLIHandler.parse_arguments(args))
    return 0
