import shutil
from pathlib import Path

class DirectoryRecreator:

    def recreateDirectory(self, dirPath: Path):
        if dirPath.exists():
            shutil.rmtree(dirPath)

        self.__safeMkDir(dirPath)

    def __safeMkDir(self, dirPath: Path):
        while True:
            try:
                dirPath.mkdir(exist_ok=True)
                break
            except PermissionError:
                continue
