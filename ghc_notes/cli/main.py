import argparse
import enum
from collections.abc import Sequence

from typing_extensions import assert_never

from . import check


class Command(enum.Enum):
    CHECK = enum.auto()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='ghc-notes')
    subparsers = parser.add_subparsers(help='subcommand help')

    parser_check = subparsers.add_parser('check')
    parser_check.set_defaults(command=Command.CHECK)
    parser_check.add_argument('path')

    args = parser.parse_args(argv)

    command: Command = args.command
    if command is Command.CHECK:
        return check.main(path=args.path)
    assert_never(command)
