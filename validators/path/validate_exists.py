from pathlib import Path

from validators.path.base_validator import BaseValidator


class ValidateExists(BaseValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = BaseValidator._expand_path(path)
        if not path.exists():
            raise ValueError(f"Path is not a file: {path}!")

        return path
