from abc import ABC, abstractmethod
from pathlib import Path


class BaseValidator(ABC):

    @staticmethod
    @abstractmethod
    def validate(path: str | Path) -> Path:
        ...

    @staticmethod
    def _expand_path(path: str | Path) -> Path:
        return Path(path).expanduser().resolve()