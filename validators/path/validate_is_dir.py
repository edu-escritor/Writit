from pathlib import Path

from validators.path.base_validator import BaseValidator


class ValidateIsDir(BaseValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = BaseValidator._expand_path(path)
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")

        return path
