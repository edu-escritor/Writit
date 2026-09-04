import re
from abc import ABC
from pathlib import Path
from shutil import copy2
from typing import Final

from modules.enums.locales import Locales
from translations.translation_factory import TranslationFactory
from validators.path.validate_exists import ValidateExists
from validators.path.validate_not_exists import ValidateNotExists


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
    def _create_folder(cls, folder: Path, keep: bool = True) -> None:
        folder.mkdir(parents=False, exist_ok=False)
        ValidateExists.validate(folder)

        if not keep:
            return

        file_keep = folder / cls.FILE_KEEP
        file_keep.touch()
        ValidateExists.validate(file_keep)

    @staticmethod
    def _create_file(file: Path, content: str | None = None) -> None:
        file.touch()
        ValidateExists.validate(file)

        if content is not None:
            file.write_text(content, encoding="utf-8")

    @staticmethod
    def _copy_file(original: Path, new: Path) -> None:
        ValidateNotExists.validate(new)
        copy2(original, new)
        ValidateExists.validate(new)

    @staticmethod
    def _replace_first_header(file: Path, title: str | None) -> None:
        if title is None:
            return

        lines = file.read_text(encoding="utf-8").splitlines(keepends=True)

        for index, line in enumerate(lines):
            stripped = line.strip()

            if not stripped:
                continue

            match = re.match(r"^(#{1,6})\s+.+$", stripped)

            if match is None:
                raise ValueError("The file does not start with a Markdown header!")

            header = match.group(1)
            line_ending = "\n" if line.endswith("\n") else ""

            lines[index] = f"{header} {title}{line_ending}"

            file.write_text("".join(lines), encoding="utf-8")
            return

        raise ValueError("The file does not contain a Markdown header!")
