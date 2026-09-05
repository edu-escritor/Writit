from pathlib import Path

from modules.project.models.project import Project
from modules.project.models.project_item import ProjectItem
from utils.parse.parse_index import ParseIndex
from utils.parse.parse_part import ParsePart
from utils.parse.parse_root import ParseRoot
from utils.parse.parse_slug import ParseSlug
from utils.parse.parse_version import ParseVersion
from validators.path.validate_exists import ValidateExists
from validators.path.validate_is_file import ValidateIsFile


class ParseProjectItem:

    @staticmethod
    def parse(path: str | Path) -> ProjectItem:
        path = ValidateExists.validate(path)
        path = ValidateIsFile.validate(path)

        root = ParseRoot().parse(path)
        project = Project.load(root)

        context = path.parent.relative_to(root)

        return ProjectItem(
            project=project,
            extension=path.suffix.lstrip("."),
            context=str(context),
            part=ParsePart().parse(path),
            index=ParseIndex().parse(path),
            version=ParseVersion().parse(path),
            slug=ParseSlug().parse(
                path=path,
                title=None,
            ),
        )
