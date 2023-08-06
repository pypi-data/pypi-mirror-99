"""
Command-line utility for translating VC-2 pseudocode listings into Python.
"""

from typing import Any

import sys

from argparse import ArgumentParser, FileType

from vc2_pseudocode_parser.parser import ParseError, ASTConstructionError

from vc2_pseudocode_parser.python_transformer import pseudocode_to_python


def main(*args: Any) -> int:
    parser = ArgumentParser(
        description="""
            Convert a VC-2 pseudocode listing into equivalent Python code.
        """
    )
    parser.add_argument(
        "pseudocode_file",
        type=FileType("r"),
        default=sys.stdin,
        nargs="?",
    )
    parser.add_argument(
        "python_file",
        type=FileType("w"),
        default=sys.stdout,
        nargs="?",
    )

    args = parser.parse_args(*args)

    try:
        python = pseudocode_to_python(
            args.pseudocode_file.read(),  # type: ignore
            add_translation_note=True,
        )
    except (ParseError, ASTConstructionError) as e:
        sys.stderr.write(f"Syntax error: {str(e)}\n")
        return 1

    args.python_file.write(f"{python}\n")  # type: ignore
    return 0


if __name__ == "__main__":
    sys.exit(main())
