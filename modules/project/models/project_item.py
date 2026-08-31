from dataclasses import dataclass
from pathlib import Path
from typing import Final

from modules.project.models.project import Project


@dataclass
class ProjectItem:

    project: Project
    extension: str = "md"
    context: str | None = None
    part: tuple[int, int] | None = None
    index: tuple[int, int] | None = None
    version: tuple[int, int] | None = None
    slug: str | None = None

    EXTENSION: Final[str] = "md"

    @property
    def name(self) -> str | None:
        parts = []

        if self.part is not None:
            part, padding = self.part
            parts.append(f"p{part:0{padding}d}")

        if self.index is not None:
            index, padding = self.index
            parts.append(f"i{index:0{padding}d}")

        if self.version is not None:
            version, padding = self.version
            parts.append(f"v{version:0{padding}d}")

        if self.slug is not None:
            parts.append(self.slug)

        if not parts:
            return None

        return "_".join(parts) + f".{self.extension}"

    @property
    def path(self) -> Path | None:
        name = self.name
        if name is None:
            return None

        path = self.project.root

        if self.context is not None:
            path /= self.context

        return path / name
