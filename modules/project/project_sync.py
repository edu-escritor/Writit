from pathlib import Path

from modules.enums.project_type import ProjectType
from modules.project.base_project import BaseProject
from modules.project.models.project import Project
from utils.parse_root import ParseRoot


class ProjectSync(BaseProject):

    def execute(
        self,
        root: str | Path,
        title: str,
        project_type: ProjectType = ProjectType.STANDALONE,
        parts: int = 0,
    ) -> str:
        root = ParseRoot().parse(root)
        project = Project.load(root)
