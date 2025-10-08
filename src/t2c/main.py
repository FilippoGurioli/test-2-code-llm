import sys

from t2c.cli.cli_handler import CLIHandler
from t2c.cli.validation_chain.chain_validator import ChainValidator


def main(args: list[str] | None = None) -> int:
    """Main entry point."""
    if args is None:
        args = sys.argv[1:]

    cli_handler = CLIHandler(_create_validator())

    print(cli_handler.validate_configuration(cli_handler.parse_arguments(args)))
    return 0


def _create_validator() -> ChainValidator:
    chain_validator = ChainValidator()
    # chain_validator.add_validator(PathValidator())
    # chain_validator.add_validator(ModelValidator())
    # chain_validator.add_validator(DependencyValidator())
    # chain_validator.add_validator(ResourceValidator())
    return chain_validator
