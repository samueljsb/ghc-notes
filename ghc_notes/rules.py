from collections import defaultdict
from collections.abc import Collection
from typing import TypeVar

from ghc_notes.model import Definition
from ghc_notes.model import Reference


class DuplicateDefinitions:
    """Each title may be used to define a single note.

    Two different notes should not have the same title. If they do, references
    to the note are ambiguous.
    """

    def check(
        self,
        definitions: Collection[Definition],
        references: object,  # noqa: ARG002
    ) -> tuple[Definition | Reference, ...]:
        return tuple(
            definition
            for definitions_by_name in _group_by_title(definitions).values()
            for definition in definitions_by_name
            if len(definitions_by_name) > 1
        )


class OrphanedReferences:
    """All references must refer to an existing note.

    A reference to a note that does not exist is probably a mistake.
    """

    def check(
        self,
        definitions: Collection[Definition],
        references: Collection[Reference],
    ) -> tuple[Definition | Reference, ...]:
        defined_titles = {
            definition.title.casefold() for definition in definitions
        }
        return tuple(
            reference
            for title, definitions_by_name in _group_by_title(
                references
            ).items()
            for reference in definitions_by_name
            if title.casefold() not in defined_titles
        )


_TNote = TypeVar('_TNote', bound=(Definition | Reference))


def _group_by_title(
    notes: Collection[_TNote],
) -> dict[str, tuple[_TNote, ...]]:
    notes_by_title: defaultdict[str, tuple[_TNote, ...]] = defaultdict(tuple)
    for note in notes:
        notes_by_title[note.title.casefold()] += (note,)
    return dict(notes_by_title)
