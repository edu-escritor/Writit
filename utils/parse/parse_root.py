from pathlib import Path

from modules.project.models.project import Project
from validators.path.validate_exists import ValidateExists


class ParseRoot:

    # noinspection PyMethodMayBeStatic
    def parse(self, path: str | Path) -> Path:
        path = ValidateExists.validate(path)

        for folder in (path, *path.parents):
            if (folder / Project.FILE).is_file():
                return folder

        raise ValueError(f"{path} is not a valid project root!")
