import os.path

from ghc_notes import find

project_dir = os.path.dirname(os.path.dirname(__file__))
test_project = os.path.join(project_dir, 'test_project')


class TestNoteFinder:
    def test_finds_notes_in_test_project(self) -> None:
        finder = find.NoteFinder()

        notes = finder.find_notes(test_project)

        assert notes == (
            find.Note(
                title='This is a test note',
                definitions=(find.Location('module.py', 3),),
                references=(find.Location('module.py', 15),),
            ),
        )
