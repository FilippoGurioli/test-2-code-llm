"""The main module. It contains the entrance for the tool.

Returns:
    int: The exit code.
"""

import os
import sys
import traceback
from pathlib import Path

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
        print("Error during execution of Test 2 Code:")
        print(_format_filtered_traceback(e))
        return 1


def _create_chain_validator() -> ChainValidator:
    chain_validator = ChainValidator()
    chain_validator.add_validator(CommandValidator())
    chain_validator.add_validator(PathValidator())
    chain_validator.add_validator(ModelValidator())
    chain_validator.add_validator(DependencyValidator())
    chain_validator.add_validator(YamlValidator())
    return chain_validator


def _format_filtered_traceback(exc: Exception) -> str:
    """The function inspects the traceback and keeps frames that appear to be under the
    repository source directory. If no
    project frames are found, the full traceback is returned as a fallback.
    """
    tb_list = traceback.extract_tb(exc.__traceback__)
    cwd = Path.cwd()
    project_frames = []

    for fr in tb_list:
        fname = Path(fr.filename)
        path_str = str(fname)

        if (
            "site-packages" in path_str
            or "dist-packages" in path_str
            or "/usr/lib/python" in path_str
            or "/usr/local/lib/python" in path_str
        ):
            continue

        try:
            rel = fname.relative_to(cwd)
            rel_str = str(rel)
        except Exception:
            rel_str = ""

        if (os.path.join("src", "t2c") in path_str) or rel_str.startswith(
            os.path.join("src", "t2c")
        ):
            project_frames.append(fr)

    if not project_frames:
        return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    lines: list[str] = ["Traceback (filtered to project code):"]
    for fr in project_frames:
        lines.append(f'  File "{fr.filename}", line {fr.lineno}, in {fr.name}')
        if fr.line:
            lines.append(f"    {fr.line.strip()}")

    lines.append(f"{type(exc).__name__}: {exc}")
    return "\n".join(lines)
