import re
from datetime import date
from importlib.resources import files
from pathlib import Path

from modules.enums.locales import Locales
from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from modules.project.models.project_item import ProjectItem
from translations.base_translation import BaseTranslation
from translations.translation_factory import TranslationFactory
from utils.file_title_handler import FileTitleHandler
from utils.parse.parse_index import ParseIndex
from utils.parse.parse_next_version import ParseNextVersion
from utils.parse.parse_project_item import ParseProjectItem
from utils.parse.parse_root import ParseRoot
from utils.parse.parse_version import ParseVersion
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
        self._manuscript_content: str = ""

    def create(self, sync: bool = False) -> None:
        template = files("modules.templates").joinpath("master.md_")
        content = template.read_text(encoding="utf-8").strip()

        content = content.replace("«title»", self._project.title)
        content = content.replace("«autorName»", self._project.author_name)
        content = content.replace("«autorEmail»", self._project.author_email)
        content = content.replace(
            "«autorCellPhone»",
            self._project.author_cellphone,
        )

        self._content = content.replace(
            "«date»",
            self.__today(),
        )

        self.__handle_standalone()
        self.__handle_chaptered()

        for part in range(1, self._project.parts + 1):
            self.__handle_parted(
                part=part,
                parts=self._project.parts,
            )

        self.__handle_word_count()

        self.__create_file(self._content)

    def __today(self) -> str:
        today = date.today()

        date_format = self._translation.translate("date.long_format")
        month = self._translation.translate(f"date.month.{today.month:02d}")

        date_format = date_format.replace(
            "«day»",
            str(today.day),
        )
        date_format = date_format.replace(
            "«month»",
            month,
        )
        date_format = date_format.replace(
            "«year»",
            str(today.year),
        )

        return date_format

    def __create_file(self, content: str) -> None:
        self._master.unlink(missing_ok=True)
        self._master.write_text(
            content,
            encoding="utf-8",
        )

        ValidateExists.validate(self._master)

    def __append_file(self, file: Path) -> None:
        content = FileTitleHandler.handle(file).strip()

        self._content += "\n\n" + content
        self._manuscript_content += "\n\n" + content

    def __handle_word_count(self) -> None:
        words = len(self._manuscript_content.split())
        formatted_words = f"{words:,}".replace(",", " ")

        self._content = self._content.replace(
            "«words»",
            formatted_words,
        )

    def __fetch_latest_by_index(
        self,
        folder: Path,
    ) -> dict[int, Path]:
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

        return {index: file for index, (_, file) in chapters.items()}

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
                self.__append_file(file)
                return

    def __handle_chaptered(self) -> None:
        if self._project.project_type != ProjectType.CHAPTERED:
            return

        folder = self._project.root / self._translation.translate("project.folder.chaptered")

        chapters = self.__fetch_latest_by_index(folder)

        for index in sorted(chapters):
            self.__append_file(chapters[index])

    def __handle_parted(
        self,
        part: int | None,
        parts: int | None,
    ) -> None:
        if self._project.project_type != ProjectType.PARTED or part is None or parts is None:
            return

        prefix = self._translation.translate("project.folder.parted")
        padding = max(
            2,
            len(str(parts)),
        )

        folder = self._project.root / f"{prefix}{part:0{padding}d}"

        part_file = folder / (
            f"p{part:03d}_" f"i0000_" f"{prefix.rstrip('_')}-{part:0{padding}d}." + ProjectItem.EXTENSION
        )

        if part_file.exists():
            self.__append_file(part_file)

        chapters = self.__fetch_latest_by_index(folder)

        for index in sorted(chapters):
            self.__append_file(chapters[index])
