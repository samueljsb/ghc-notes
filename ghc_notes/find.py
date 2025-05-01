from __future__ import annotations

import glob
import os.path
import re
from collections import defaultdict
from collections.abc import Generator
from collections.abc import Iterable
from collections.abc import Mapping
from typing import Protocol
from typing import TypeAlias

import attrs

Title: TypeAlias = str
FilePath: TypeAlias = str
LineNo: TypeAlias = int


@attrs.frozen
class Note:
    title: Title
    definitions: tuple[Location, ...]
    references: tuple[Location, ...]


@attrs.frozen
class Location:
    file: FilePath
    line: LineNo


class GlobFileFinder:
    def find_files(self, base_dir: FilePath) -> Generator[FilePath]:
        yield from glob.glob(os.path.join(base_dir, '**/*'), recursive=True)


class Parser:
    def __init__(self) -> None:
        self.re = re.compile(r'(see )?note \[(?P<title>.*)\]', re.IGNORECASE)

    def parse_notes(
        self, lines: Iterable[str]
    ) -> tuple[Mapping[Title, list[LineNo]], Mapping[Title, list[LineNo]]]:
        references = defaultdict(list)
        definitions = defaultdict(list)
        for lineno, line in enumerate(lines, start=1):
            match = self.re.search(line)
            if match is None:
                continue

            is_reference, title = match.groups()
            if is_reference:
                references[title].append(lineno)
            else:
                definitions[title].append(lineno)

        return definitions, references


class FileFinder(Protocol):
    def find_files(self, base_dir: FilePath) -> Generator[FilePath]: ...


@attrs.frozen
class NoteFinder:
    files: FileFinder = attrs.field(factory=GlobFileFinder)
    parser: Parser = attrs.field(factory=Parser)

    def find_notes(self, base_dir: FilePath) -> tuple[Note, ...]:
        definitions: defaultdict[Title, list[Location]] = defaultdict(list)
        references: defaultdict[Title, list[Location]] = defaultdict(list)
        for file in self.files.find_files(base_dir):
            if not os.path.isfile(file):
                continue

            with open(file) as f:
                defs, refs = self.parser.parse_notes(f)

            for title, line_nos in defs.items():
                definitions[title].extend(
                    Location(os.path.relpath(file, base_dir), lineno)
                    for lineno in line_nos
                )
            for title, line_nos in refs.items():
                references[title].extend(
                    Location(os.path.relpath(file, base_dir), lineno)
                    for lineno in line_nos
                )

        return tuple(
            {
                Note(
                    title,
                    definitions=tuple(definitions_),
                    references=tuple(references[title]),
                )
                for title, definitions_ in definitions.items()
            }
        )
