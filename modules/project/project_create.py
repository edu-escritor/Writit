from importlib.resources import files
from pathlib import Path

from num2words import num2words

from modules.enums.project_type import ProjectType
from modules.project.base_project import BaseProject
from modules.project.models.project import Project
from naming.slugifier import Slugifier
from validators.modules.validate_project_type_parts import ValidateProjectTypeParts
from validators.path.validate_exists import ValidateExists
from validators.path.validate_is_dir import ValidateIsDir
from validators.validate_not_empty import ValidateNotEmpty
from validators.validate_not_negative import ValidateNotNegative


class ProjectCreate(BaseProject):

    def execute(
        self,
        root: str | Path,
        title: str,
        project_type: ProjectType = ProjectType.STANDALONE,
        parts: int = 0,
    ) -> None:
        project = Project.empty()
        self.__handle_root(project=project, root=root)
        self.__handle_title_and_project_root(project=project, title=title)
        self.__handle_type_and_parts(
            project=project, project_type=project_type, parts=parts
        )

        self.__create_meta(project)
        self.__create_standalone(project)
        self.__create_chaptered(project)
        self.__create_parted(project)

        project.save()

    @staticmethod
    def __handle_root(project: Project, root: str | Path) -> None:
        root = ValidateIsDir.validate(root)
        project.root = ValidateExists.validate(root)

    @staticmethod
    def __handle_title_and_project_root(project: Project, title: str) -> None:
        title = ValidateNotEmpty.validate(title, "The project title cannot be empty!")

        slug = Slugifier.slugify(title)

        updated_root = project.root / slug

        if updated_root.exists():
            raise ValueError(f"The project folder already exists: {updated_root}")

        project.root = updated_root
        project.title = title

        project.root.mkdir(parents=False, exist_ok=False)
        ValidateExists.validate(project.root)

    @staticmethod
    def __handle_type_and_parts(
        project: Project,
        project_type: ProjectType,
        parts: int,
    ) -> None:
        parts = ValidateNotNegative.validate(parts)
        ValidateProjectTypeParts.validate(project_type, parts)

        project.parts = parts
        project.project_type = project_type

    def __create_meta(self, project: Project) -> None:
        folder = project.root / self.FOLDER_META
        self._create_folder(folder)

        if project.project_type == ProjectType.STANDALONE:
            return

        file_resume = folder / self.FILE_RESUME

        template = files("modules.templates").joinpath("resume.md_")
        content = template.read_text(encoding="utf-8")

        self._create_file(file_resume, content)

    def __create_standalone(self, project: Project) -> None:
        if project.project_type != ProjectType.STANDALONE:
            return

        folder = project.root / self.FOLDER_STANDALONE
        self._create_folder(folder, keep=False)

        slug = Slugifier.slugify(project.title)

        filename = f"v001_{slug}.md"
        file = folder / filename

        template = files("modules.templates").joinpath("chapter.md_")
        content = template.read_text(encoding="utf-8")
        content = content.replace("«title»", project.title)

        self._create_file(file, content)

    def __create_chaptered(self, project: Project) -> None:
        if project.project_type != ProjectType.CHAPTERED:
            return

        folder = project.root / self.FOLDER_CHAPTERED
        self._create_folder(folder)

    def __create_parted(self, project: Project) -> None:
        if project.project_type != ProjectType.PARTED:
            return

        width = max(2, len(str(project.parts)))

        for part in range(1, project.parts + 1):
            folder = project.root / f"{self.FOLDER_PARTED}{part:0{width}d}"

            self._create_folder(folder, keep=False)

            template = files("modules.templates").joinpath("part.md_")
            content = template.read_text(encoding="utf-8")

            number = str(num2words(part, lang="pt_PT")).capitalize()

            content = content.replace("«number»", number)

            filename = f"p{part:03d}_" f"i0000_" f"parte-{part:0{width}d}.rst"

            file = folder / filename

            self._create_file(file, content)
