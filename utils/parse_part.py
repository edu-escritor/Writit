import re
from pathlib import Path

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from utils.parse_root import ParseRoot
from validators.path.validate_exists import ValidateExists


class ParsePart:

    # noinspection PyMethodMayBeStatic
    def parse(self, path: str | Path) -> tuple[int, int] | None:
        path = ValidateExists.validate(path)
        root = ParseRoot().parse(path)
        project = Project.load(root)
        if ProjectType.PARTED != project.project_type:
            return None

        if path.is_dir():
            match = re.search(r"^part(e?)_(\d+)$", path.name)

            if match:
                raw_part = match.group(2)

                return (
                    int(raw_part),
                    len(raw_part),
                )

        match = re.search(r"(?:^|_)p(\d+)(?:_|$)", path.name)
        if match:
            raw_part = match.group(1)

            return (
                int(raw_part),
                len(raw_part),
            )

        return None
