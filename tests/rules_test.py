from ghc_notes import rules
from ghc_notes.model import Definition
from ghc_notes.model import Reference


class TestDuplicateDefinitions:
    def test_allows_different_titles(self) -> None:
        rule = rules.DuplicateDefinitions()

        results = rule.check(
            definitions=(
                Definition(title='A note title', file='path/to/file', line=1),
                Definition(
                    title='A different title', file='path/to/file', line=2
                ),
            ),
            references=(),
        )

        assert results == ()

    def test_detects_exact_match(self) -> None:
        rule = rules.DuplicateDefinitions()

        results = rule.check(
            definitions=(
                Definition(title='A note title', file='path/to/file', line=1),
                Definition(title='A note title', file='path/to/file', line=2),
            ),
            references=(),
        )

        assert results == (
            Definition(title='A note title', file='path/to/file', line=1),
            Definition(title='A note title', file='path/to/file', line=2),
        )

    def test_detects_match_with_different_case(self) -> None:
        rule = rules.DuplicateDefinitions()

        results = rule.check(
            definitions=(
                Definition(title='A note title', file='path/to/file', line=1),
                Definition(title='a NoTe TiTlE', file='path/to/file', line=2),
            ),
            references=(),
        )

        assert results == (
            Definition(title='A note title', file='path/to/file', line=1),
            Definition(title='a NoTe TiTlE', file='path/to/file', line=2),
        )


class TestOrphanedReferences:
    def test_allows_references_with_definition(self) -> None:
        rule = rules.OrphanedReferences()

        results = rule.check(
            definitions=(
                Definition(title='A note title', file='path/to/file', line=1),
            ),
            references=(
                Reference(title='A note title', file='path/to/file', line=2),
            ),
        )

        assert results == ()

    def test_allows_reference_with_different_case_to_definition(self) -> None:
        rule = rules.OrphanedReferences()

        results = rule.check(
            definitions=(
                Definition(title='A note title', file='path/to/file', line=1),
            ),
            references=(
                Reference(title='a NoTe TiTlE', file='path/to/file', line=2),
            ),
        )

        assert results == ()

    def test_detects_references_without_definition(self) -> None:
        rule = rules.OrphanedReferences()

        results = rule.check(
            definitions=(
                Definition(title='A note title', file='path/to/file', line=1),
            ),
            references=(
                Reference(
                    title='A different title', file='path/to/file', line=2
                ),
                Reference(title='Another title', file='path/to/file', line=3),
            ),
        )

        assert results == (
            Reference(title='A different title', file='path/to/file', line=2),
            Reference(title='Another title', file='path/to/file', line=3),
        )
