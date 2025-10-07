import sys

from t2c.cli.parsing.argument_parser import ArgumentParser


def main(args: list[str] | None = None) -> int:
    """Main entry point."""
    if args is None:
        args = sys.argv[1:]

    config = ArgumentParser.parse(args)
    print(config)
    return 0
