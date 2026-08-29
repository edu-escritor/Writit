from importlib.resources import files
from pathlib import Path

from num2words import num2words

from modules.enums.project_type import ProjectType
from modules.project.base_project import BaseProject
from modules.project.models.project import Project


class ProjectAddPart(BaseProject):

    def execute(self, root: str | Path) -> None:
        project = Project.load(root)
        if project.project_type != ProjectType.PARTED:
            raise ValueError(f"The project does not have parts!")

        new_part = project.parts + 1
        width = max(2, len(str(project.parts)))

        folder = project.root / f"{self.FOLDER_PARTED}{new_part:0{width}d}"

        self._create_folder(folder, keep=False)

        template = files("modules.templates").joinpath("part.md_")
        content = template.read_text(encoding="utf-8")

        number = str(num2words(new_part, lang="pt_PT")).capitalize()

        content = content.replace("«number»", number)

        filename = f"p{new_part:03d}_" f"i0000_" f"parte-{new_part:0{width}d}.rst"

        file = folder / filename

        self._create_file(file, content)
