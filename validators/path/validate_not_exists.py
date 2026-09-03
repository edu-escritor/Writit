from pathlib import Path

from validators.path.base_validator import BaseValidator


class ValidateNotExists(BaseValidator):

    @staticmethod
    def validate(path: str | Path) -> Path:
        path = BaseValidator._expand_path(path)

        if path.exists():
            raise ValueError(f"Path already exists: {path}!")

        return path
