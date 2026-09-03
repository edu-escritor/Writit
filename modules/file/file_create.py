from importlib.resources import files
from pathlib import Path

from modules.project.models.project import Project
from modules.project.models.project_item import ProjectItem
from naming.slugifier import Slugifier
from utils.parse_next_index import ParseNextIndex
from utils.parse_root import ParseRoot
from validators.path.validate_exists import ValidateExists
from validators.path.validate_is_dir import ValidateIsDir
from validators.path.validate_not_exists import ValidateNotExists


class FileCreate:

    def execute(self, path: str | Path, title: str, part: int | None) -> None:
        project_item = self.__build_project_item(
            path=path,
            title=title,
            part=part,
        )

        to_create = project_item.path

        if to_create is None:
            raise ValueError("Something went wrong with the project item creation!")

        ValidateNotExists.validate(to_create)

        self.__handle_content(
            path=to_create,
            title=title,
        )

    @staticmethod
    def __build_project_item(
        path: str | Path,
        title: str,
        part: int | None,
    ) -> ProjectItem:
        path = ValidateExists.validate(path)

        if path.is_file():
            path = path.parent

        path = ValidateIsDir.validate(path)

        root = ParseRoot().parse(path)

        if root == path:
            raise ValueError("It's not possible to create a file in the project root!")

        project = Project.load(root)
        context = path.relative_to(root)
        slug = Slugifier.slugify(title)

        parsed_part = (part, 3) if part is not None else None

        project_item = ProjectItem(
            project=project,
            context=str(context),
            part=parsed_part,
            version=(1, 3),
            slug=slug,
        )

        index = ParseNextIndex().parse(project_item)

        if index is not None:
            project_item.index = (index, 4)

        return project_item

    @staticmethod
    def __handle_content(path: Path, title: str) -> None:
        template = files("modules.templates").joinpath("chapter.md_")
        content = template.read_text(encoding="utf-8")
        content = content.replace("«title»", title)

        path.write_text(content, encoding="utf-8")
