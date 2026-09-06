import json
import tempfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import ClassVar, Self

from modules.enums.locales import Locales
from modules.enums.project_type import ProjectType
from naming.slugifier import Slugifier
from validators.path.validate_is_file import ValidateIsFile


@dataclass
class Project:
    FILE: ClassVar[str] = ".writit_project"

    title: str
    root: Path
    project_type: ProjectType
    parts: int
    locale: Locales = Locales.PORTUGUESE_EUROPEAN
    author_name: str = "John Doe"
    author_email: str = "john.doe@gmail.com"
    author_cellphone: str = "+351 999 999 999"
    created_at: date = field(default_factory=date.today)

    def save(self) -> None:
        data = {
            "title": self.title,
            "root": str(self.root),
            "project_type": self.project_type.value,
            "parts": self.parts,
            "locale": self.locale.value,
            "created_at": self.created_at.isoformat(),
        }

        path = self.root / self.FILE

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @property
    def slug(self) -> str:
        return Slugifier.slugify(self.title)

    @classmethod
    def load(cls, root: str | Path) -> Self:
        root = Path(root)
        path = root / cls.FILE

        path = ValidateIsFile.validate(path)

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return cls(
            title=data["title"],
            root=root,
            project_type=ProjectType(data["project_type"]),
            parts=data["parts"],
            locale=Locales(data["locale"]),
            created_at=date.fromisoformat(data["created_at"]),
        )

    @classmethod
    def empty(cls) -> Self:
        return cls(
            title="Default",
            root=Path(tempfile.gettempdir()),
            project_type=ProjectType.STANDALONE,
            parts=0,
        )
