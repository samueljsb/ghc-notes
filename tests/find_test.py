from collections.abc import Generator
from collections.abc import Mapping

import attrs

from ghc_notes import find
from ghc_notes.model import Definition
from ghc_notes.model import Reference


@attrs.frozen
class Files:
    files: Mapping[str, str] = attrs.field(factory=dict)  # filename: content

    def get_files(self, path: str) -> Generator[tuple[str, str]]:  # noqa: ARG002
        yield from self.files.items()


class TestFindNotes:
    def test_no_files(self) -> None:
        finder = find.Finder(files=Files())

        definitions, references = finder.find_notes('.')

        assert definitions == ()
        assert references == ()

    def test_files_with_no_notes(self) -> None:
        finder = find.Finder(
            files=Files(
                {
                    'a/file': '',
                    'another/file': """\
# Note [This is a note]
# ~~~~~~~~~~~~~~~~~~~~~
# It doesn't say much.
""",
                    'a_different/file': """\
This references a note.
See Note [This is a note]
""",
                }
            )
        )

        definitions, references = finder.find_notes('.')

        assert (definitions, references) == (
            (Definition(title='This is a note', file='another/file', line=1),),
            (
                Reference(
                    title='This is a note', file='a_different/file', line=2
                ),
            ),
        )
