from abc import ABC
from pathlib import Path
from typing import Final

from modules.enums.locales import Locales
from translations.translation_factory import TranslationFactory
from validators.path.validate_exists import ValidateExists


class BaseProject(ABC):

    FILE_KEEP: Final[str] = ".gitkeep"
    FILE_RESUME: Final[str] = "project.file.resume"

    FOLDER_META: Final[str] = "project.folder.meta"
    FOLDER_PARTED: Final[str] = "project.folder.parted"
    FOLDER_CHAPTERED: Final[str] = "project.folder.chaptered"
    FOLDER_STANDALONE: Final[str] = "project.folder.standalone"

    def __init__(self, locale: Locales) -> None:
        self._locale = locale
        self._translation = TranslationFactory.get(locale)

    @classmethod
    def _create_folder(
        cls,
        folder: Path,
        keep: bool = True,
    ) -> None:
        folder.mkdir(parents=False, exist_ok=False)
        ValidateExists.validate(folder)

        if not keep:
            return

        file_keep = folder / cls.FILE_KEEP
        file_keep.touch()
        ValidateExists.validate(file_keep)

    @staticmethod
    def _create_file(
        file: Path,
        content: str | None = None,
    ) -> None:
        file.touch()
        ValidateExists.validate(file)

        if content is not None:
            file.write_text(content, encoding="utf-8")
