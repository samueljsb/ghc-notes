import sys
from collections.abc import Collection
from typing import Protocol

import attrs

from ghc_notes import files
from ghc_notes import find
from ghc_notes import rules
from ghc_notes.model import Definition
from ghc_notes.model import Reference


def main(path: str) -> int:
    finder = find.Finder(files=files.FileSystem())

    check_notes = Check(
        finder=finder,
        rules_to_check=(
            rules.DuplicateDefinitions(),
            rules.OrphanedReferences(),
        ),
    )
    try:
        check_notes(path)
    except ProblemsFound:
        return 1
    else:
        return 0


class Finder(Protocol):
    def find_notes(
        self, path: str
    ) -> tuple[tuple[Definition, ...], tuple[Reference, ...]]: ...


class Rule(Protocol):
    def check(
        self,
        definitions: Collection[Definition],
        references: Collection[Reference],
    ) -> tuple[Definition | Reference, ...]: ...


class ProblemsFound(Exception):
    pass


@attrs.frozen
class Check:
    finder: Finder
    rules_to_check: tuple[Rule, ...]

    def __call__(self, path: str) -> None:
        self.info('-> searching for notes ...')
        finder = find.Finder(files=files.FileSystem())
        definitions, references = finder.find_notes(path)
        self.info(
            f'... found {len(definitions)} definitions and {len(references)} references',  # noqa: E501
        )

        exc = None
        for rule in self.rules_to_check:
            rule_name = type(rule).__name__
            self.info(f'-> checking {rule_name!r} ...')
            violations = rule.check(definitions, references)

            if violations:
                self.info('... FAIL')
                for v in sorted(
                    violations, key=lambda v: (v.title, v.file, v.line)
                ):
                    print(
                        f'{v.file}:{v.line}: error: {rule_name}: {v.title!r}'
                    )
                exc = ProblemsFound
            else:
                self.info('... OK')

        if exc:
            raise exc

    def info(self, msg: str) -> None:
        print(msg, file=sys.stderr)
