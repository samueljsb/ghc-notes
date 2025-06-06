import glob
import os.path
from collections.abc import Generator
from typing import TypeAlias

FileName: TypeAlias = str
FileContent: TypeAlias = str


class FileSystem:
    def get_files(self, path: str) -> Generator[tuple[FileName, FileContent]]:
        for filename in glob.glob('**/*', root_dir=path, recursive=True):
            filepath = os.path.join(path, filename)
            if not os.path.isfile(filepath):
                continue
            with open(filepath) as f:
                try:
                    content = f.read()
                # Some file types cannot be read, so we skip those.
                except UnicodeDecodeError:  # pragma: no cover
                    continue
            yield filename, content
