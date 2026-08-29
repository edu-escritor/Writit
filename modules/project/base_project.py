from abc import ABC
from pathlib import Path
from typing import Final

from validators.path.validate_exists import ValidateExists


class BaseProject(ABC):

    FILE_KEEP: Final[str] = ".gitkeep"
    FILE_RESUME: Final[str] = "resumo.md"

    FOLDER_META: Final[str] = "meta"
    FOLDER_PARTED: Final[str] = "parte_"
    FOLDER_CHAPTERED: Final[str] = "capitulos"
    FOLDER_STANDALONE: Final[str] = "texto"

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
