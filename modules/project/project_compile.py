import subprocess
from datetime import date
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Final

from modules.enums.project_type import ProjectType
from modules.project.base_project import BaseProject
from modules.project.models.project import Project
from utils.parse.parse_root import ParseRoot
from validators.path.validate_exists import ValidateExists
from validators.path.validate_is_file import ValidateIsFile


class ProjectCompile(BaseProject):

    PANDOC: Final[str] = "/usr/bin/pandoc"
    OPTIONS: Final[tuple[str, ...]] = (
        "markdown",
        "-auto_identifiers",
        "-hard_line_breaks",
    )

    def execute(
        self,
        root: str | Path,
    ) -> str:
        root = ParseRoot().parse(root)
        project = Project.load(root)

        source_file = ValidateIsFile.validate(root / "master.md")

        compiled_file = root / (project.slug + "_" + date.today().isoformat() + ".odt")

        compiled_file.unlink(missing_ok=True)

        template_resource = self.__fetch_template(project)
        template = self.__create_temp_template(template_resource)

        try:
            command = self.__build_command(
                source_file=source_file,
                compiled_file=compiled_file,
                template=template,
            )

            subprocess.run(
                command,
                check=True,
            )
        finally:
            template.unlink(missing_ok=True)

        ValidateExists.validate(compiled_file)

        return f"The project was successfully compiled to {compiled_file}!"

    def __build_command(
        self,
        source_file: Path,
        compiled_file: Path,
        template: Path,
    ) -> list[str]:
        options = "".join(self.OPTIONS)

        return [
            self.PANDOC,
            str(source_file),
            "-f",
            options,
            "-t",
            "odt",
            f"--reference-doc={template}",
            "-o",
            str(compiled_file),
        ]

    @staticmethod
    def __create_temp_template(template: Traversable) -> Path:
        with NamedTemporaryFile(
            suffix=".odt",
            delete=False,
        ) as temp:
            temp.write(template.read_bytes())

            return Path(temp.name)

    @staticmethod
    def __fetch_template(project: Project) -> Traversable:
        templates = files("modules.templates.libre_office")

        if project.project_type == ProjectType.STANDALONE:
            return templates.joinpath("standalone_pt_pt.odt")

        if project.project_type == ProjectType.CHAPTERED:
            return templates.joinpath("chaptered_pt_pt.odt")

        return templates.joinpath("part_pt_pt.odt")
