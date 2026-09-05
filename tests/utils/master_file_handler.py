import re
from datetime import date
from importlib.resources import files
from pathlib import Path

from modules.enums.locales import Locales
from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from modules.project.models.project_item import ProjectItem
from tests.utils.file_title_handler import FileTitleHandler
from translations.base_translation import BaseTranslation
from translations.translation_factory import TranslationFactory
from utils.parse_index import ParseIndex
from utils.parse_next_version import ParseNextVersion
from utils.parse_project_item import ParseProjectItem
from utils.parse_root import ParseRoot
from utils.parse_version import ParseVersion
from validators.path.validate_exists import ValidateExists


class MasterFileHandler:
    MASTER = "master.md"

    def __init__(
        self,
        root: str | Path,
        locale: Locales = Locales.PORTUGUESE_EUROPEAN,
    ) -> None:
        root = ParseRoot().parse(root)

        self._project: Project = Project.load(root)
        self._locale: Locales = locale
        self._translation: type[BaseTranslation] = TranslationFactory.get(locale)
        self._master: Path = self._project.root / self.MASTER
        self._content: str = ""

    def create(self, sync: bool = False) -> None:
        # @todo: implement locale logic
        template = files("modules.templates").joinpath("master.md_")
        content = template.read_text(encoding="utf-8").strip()

        content = content.replace("«title»", self._project.title)
        content = content.replace("«autorName»", self._project.author_name)
        content = content.replace("«autorEmail»", self._project.author_email)
        content = content.replace("«autorCellPhone»", self._project.author_cellphone)
        self._content = content.replace("«date»", self.__today())
        self.__handle_standalone()
        self.__handle_chaptered()

        self.__create_file(content)

    def __today(self) -> str:
        today = date.today()

        date_format = self._translation.translate("date.long_format")
        month = self._translation.translate(f"date.month.{today.month:02d}")

        date_format = date_format.replace("«day»", str(today.day))
        date_format = date_format.replace("«month»", month)
        date_format = date_format.replace("«year»", str(today.year))

        return date_format

    def __create_file(self, content: str) -> None:
        self._master.unlink(missing_ok=True)
        self._master.write_text(content, encoding="utf-8")

        ValidateExists.validate(self._master)

    def __fetch_context(self) -> list[Path]:
        folders: list[Path] = []

        folder = self._project.root

        match self._project.project_type:
            case ProjectType.STANDALONE:
                folders.append(folder / self._translation.translate("project.folder.standalone"))

            case ProjectType.CHAPTERED:
                folders.append(folder / self._translation.translate("project.folder.chaptered"))

            case ProjectType.PARTED:
                prefix = self._translation.translate("project.folder.parted")

                for part in range(1, self._project.parts + 1):
                    folders.append(folder / f"{prefix}{part:02d}")

        return folders

    def __sync_files(self, folders: list[Path]):
        for folder in folders:
            project_item = ProjectItem(project=self._project)

    def __handle_standalone(self) -> None:
        if self._project.project_type != ProjectType.STANDALONE:
            return

        folder = self._project.root / self._translation.translate("project.folder.standalone")

        max_version: int | None = None

        for file in folder.iterdir():
            if not file.is_file() or not re.match(
                r"^v\d+_.*\." + ProjectItem.EXTENSION + "$",
                file.name,
            ):
                continue

            project_item = ParseProjectItem.parse(file)

            if max_version is None:
                max_version = ParseNextVersion.parse(project_item) - 1

            current_version = ParseVersion().parse(file)

            if current_version is not None and current_version[0] == max_version:
                self._content += "\n\n" + FileTitleHandler.handle(file).strip()
                return

    def __handle_chaptered(self) -> None:
        if self._project.project_type != ProjectType.CHAPTERED:
            return

        folder = self._project.root / self._translation.translate("project.folder.chaptered")

        chapters: dict[int, tuple[int, Path]] = {}

        for file in folder.iterdir():
            if not file.is_file():
                continue

            index = ParseIndex().parse(file)
            version = ParseVersion().parse(file)

            if index is None or version is None:
                continue

            index_value = index[0]
            version_value = version[0]

            if index_value not in chapters or version_value > chapters[index_value][0]:
                chapters[index_value] = (
                    version_value,
                    file,
                )

        for index in sorted(chapters):
            _, file = chapters[index]

            self._content += "\n\n" + FileTitleHandler.handle(file).strip()

    def __handle_parted(self, part: int | None, parts: int | None) -> None:
        if self._project.project_type != ProjectType.PARTED or part is None or parts is None:
            return

        prefix = self._translation.translate("project.folder.parted")
        padding = max(2, len(str(parts)))

        folder = self._project.root / f"{prefix}{part:0{padding}d}"
