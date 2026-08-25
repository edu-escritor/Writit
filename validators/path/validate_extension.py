from pathlib import Path
from typing import Final

from validators.path.base_validator import BaseValidator
from validators.path.validate_is_file import ValidateIsFile


class ValidateExtension(BaseValidator):

    VALID_EXTENSIONS: Final[tuple[str, ...]] = (
        "md",
        "rst",
        "tex",
    )

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = BaseValidator._expand_path(path)
        ValidateIsFile.validate(path)
        suffix = path.suffix.lstrip(".")
        if not suffix in ValidateExtension.VALID_EXTENSIONS:
            raise ValueError(f"The extension {suffix} is invalid!")

        return path
