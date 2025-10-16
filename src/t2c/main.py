import sys

from t2c.cli.cli_handler import CLIHandler
from t2c.cli.validation_chain.chain_validator import ChainValidator
from t2c.cli.validation_chain.validators.command_validator import CommandValidator
from t2c.cli.validation_chain.validators.dependency_validator import DependencyValidator
from t2c.cli.validation_chain.validators.model_validator import ModelValidator
from t2c.cli.validation_chain.validators.path_validator import PathValidator
from t2c.cli.validation_chain.validators.yaml_validator import YamlValidator


def main(args: list[str] | None = None) -> int:
    """Main entry point."""
    if args is None:
        args = sys.argv[1:]

    try:
        cli_handler = CLIHandler(_create_chain_validator())
        parsed_args = cli_handler.parse_arguments(args)
        validated_args = cli_handler.validate_configuration(parsed_args)
        cli_handler.execute_command(validated_args)
        return 0
    except Exception as e:
        print(f"Error during execution of Test 2 Code: {e}")
        return 1


def _create_chain_validator() -> ChainValidator:
    chain_validator = ChainValidator()
    chain_validator.add_validator(CommandValidator())
    chain_validator.add_validator(PathValidator())
    chain_validator.add_validator(ModelValidator())
    chain_validator.add_validator(DependencyValidator())
    chain_validator.add_validator(YamlValidator())
    return chain_validator
