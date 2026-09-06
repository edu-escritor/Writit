from pathlib import Path

from modules.project.base_project import BaseProject
from modules.project.models.project import Project
from modules.project.project_compile import ProjectCompile
from utils.master_file_handler import MasterFileHandler
from utils.parse.parse_root import ParseRoot


class ProjectSync(BaseProject):

    def execute(
        self,
        root: str | Path,
        compile_master: bool = False,
    ) -> str:
        root = ParseRoot().parse(root)
        project = Project.load(root)

        MasterFileHandler(
            root=project.root,
            locale=self._locale,
        ).create(sync=True)

        if compile_master:
            message = ProjectCompile(self._locale).execute(root)

            return f"The project {project.root} was successfully synchronized. " f"{message}"

        return f"The project {project.root} was successfully synchronized!"
