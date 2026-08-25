from pathlib import Path

from validators.path.base_validator import BaseValidator


class ValidateIsFile(BaseValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = BaseValidator._expand_path(path)
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}!")

        return path
