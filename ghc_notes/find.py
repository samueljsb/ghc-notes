import re
from collections.abc import Generator
from typing import Protocol
from typing import TypeAlias

import attrs

from ghc_notes.model import Definition
from ghc_notes.model import Reference

FileName: TypeAlias = str
FileContent: TypeAlias = str


class FileSystem(Protocol):
    def get_files(
        self, path: str
    ) -> Generator[tuple[FileName, FileContent]]: ...


@attrs.frozen(init=False)
class Finder:
    files: FileSystem
    re: re.Pattern[str]

    def __init__(self, files: FileSystem) -> None:
        self.__attrs_init__(
            files=files,
            re=re.compile(r'(see )?note \[(?P<title>.*)\]', re.IGNORECASE),
        )

    def find_notes(
        self, path: str
    ) -> tuple[tuple[Definition, ...], tuple[Reference, ...]]:
        definitions = []
        references = []

        for file_name, file_content in self.files.get_files(path):
            for lineno, line in enumerate(file_content.splitlines(), start=1):
                match = self.re.search(line)
                if match is None:
                    continue

                is_reference, title = match.groups()
                if is_reference:
                    references.append(
                        Reference(title=title, file=file_name, line=lineno)
                    )
                else:
                    definitions.append(
                        Definition(title=title, file=file_name, line=lineno)
                    )

        return tuple(definitions), tuple(references)
