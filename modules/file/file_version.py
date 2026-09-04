from copy import deepcopy
from pathlib import Path

from modules.enums.locales import Locales
from modules.project.base_project import BaseProject
from modules.project.models.project_item import ProjectItem
from naming.slugifier import Slugifier
from utils.parse_next_version import ParseNextVersion
from utils.parse_project_item import ParseProjectItem
from validators.path.validate_exists import ValidateExists
from validators.path.validate_is_file import ValidateIsFile
from validators.path.validate_not_exists import ValidateNotExists


class FileVersion(BaseProject):

    def __init__(self, locale: Locales) -> None:
        super().__init__(locale)

    def execute(self, path: str | Path, title: str | None = None) -> str:
        path = ValidateExists.validate(path)
        path = ValidateIsFile.validate(path)

        original_project_item = ParseProjectItem().parse(path)
        project_item = deepcopy(original_project_item)

        self.__handle_version(project_item)
        self.__handle_title(project_item, title)

        ValidateNotExists.validate(project_item.path)

        self.__duplicate_file(
            project_item=project_item,
            original_project_item=original_project_item,
            title=title,
        )

        return f"The version {project_item.path} was successfully created!"

    @staticmethod
    def __handle_version(project_item: ProjectItem) -> None:
        version = ParseNextVersion().parse(project_item)

        project_item.version = (
            version,
            max(2, len(str(version))),
        )

    @staticmethod
    def __handle_title(
        project_item: ProjectItem,
        title: str | None,
    ) -> None:
        if title is None:
            return

        project_item.slug = Slugifier.slugify(title)

    @staticmethod
    def __duplicate_file(
        project_item: ProjectItem,
        original_project_item: ProjectItem,
        title: str | None,
    ) -> None:
        BaseProject._copy_file(
            original=original_project_item.path,
            new=project_item.path,
        )

        BaseProject._replace_first_header(
            file=project_item.path,
            title=title,
        )
