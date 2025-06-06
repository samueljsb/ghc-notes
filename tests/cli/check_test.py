from pathlib import Path

import pytest

from ghc_notes.cli import main as cli

FAKE_PROJECTS = Path(__file__).parent.parent.parent / 'fake_projects'
GOOD_PROJECT = FAKE_PROJECTS / 'good'
HAS_ERRORS_PROJECT = FAKE_PROJECTS / 'has_errors'


def test_reports_no_errors(capsys: pytest.CaptureFixture[str]) -> None:
    ret = cli.main(['check', str(GOOD_PROJECT)])

    assert ret == 0

    captured = capsys.readouterr()
    assert captured.out == ''
    assert (
        captured.err
        == """\
-> searching for notes ...
... found 1 definitions and 1 references
-> checking 'DuplicateDefinitions' ...
... OK
-> checking 'OrphanedReferences' ...
... OK
"""
    )


def test_reports_errors(capsys: pytest.CaptureFixture[str]) -> None:
    ret = cli.main(['check', str(HAS_ERRORS_PROJECT)])

    assert ret == 1

    captured = capsys.readouterr()
    assert (
        captured.out
        == """\
foo/bar.py:3: error: DuplicateDefinitions: 'This project has errors'
foo/bar.py:7: error: DuplicateDefinitions: 'This project has errors'
baz.py:2: error: OrphanedReferences: "This isn't a note"
"""
    )
    assert (
        captured.err
        == """\
-> searching for notes ...
... found 2 definitions and 1 references
-> checking 'DuplicateDefinitions' ...
... FAIL
-> checking 'OrphanedReferences' ...
... FAIL
"""
    )
