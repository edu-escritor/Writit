from pathlib import Path

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from modules.project.models.project_item import ProjectItem
from modules.project.project_create import ProjectCreate
from naming.slugifier import Slugifier
from translations.translation_factory import TranslationFactory
from utils.parse_part import ParsePart
from utils.parse_root import ParseRoot
from validators.path.validate_exists import ValidateExists
from validators.validate_not_empty import ValidateNotEmpty


class ParseProjectItem:

    @staticmethod
    def parse(path: str | Path, title: str, part: int | None = None) -> ProjectItem:
        path = ValidateExists.validate(path)
        root = ParseRoot().parse(path)
        project = Project.load(root)

        project_item = ProjectItem(project=project, extension=ProjectItem.EXTENSION)
        ParseProjectItem.__parse_part(project_item=project_item, path=path, part=part)
        ParseProjectItem.__parse_slug(project_item=project_item, title=title)
        ParseProjectItem.__parse_context(project_item=project_item)

        return project_item

    @staticmethod
    def __parse_part(project_item: ProjectItem, path: Path, part: int | None) -> None:
        project = project_item.project

        if project.project_type != ProjectType.PARTED:
            return

        if part is not None:
            project_item.part = (
                part,
                len(str(project.parts)),
            )
            return

        project_item.part = ParsePart().parse(path)

    @staticmethod
    def __parse_slug(project_item: ProjectItem, title: str) -> None:
        title = ValidateNotEmpty.validate(title)
        project_item.slug = Slugifier.slugify(title)

    @staticmethod
    def __parse_context(project_item: ProjectItem) -> None:
        project = project_item.project
        translation = TranslationFactory.get(project.locale)

        if project.project_type == ProjectType.STANDALONE:
            project_item.context = translation.translate(ProjectCreate.FOLDER_STANDALONE)
            return

        if project.project_type == ProjectType.CHAPTERED:
            project_item.context = translation.translate(ProjectCreate.FOLDER_CHAPTERED)
            return

        if project_item.part is None:
            raise ValueError("The project does not contain any part!")

        part, _ = project_item.part
        width = max(2, len(str(project.parts)))
        folder_prefix = translation.translate(ProjectCreate.FOLDER_PARTED)

        project_item.context = f"{folder_prefix}{part:0{width}d}"
