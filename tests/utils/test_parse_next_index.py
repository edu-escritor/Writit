import tempfile
from pathlib import Path

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from modules.project.models.project_item import ProjectItem
from utils.parse_next_index import ParseNextIndex


class TestParseNextIndex:

    def test_parse_next_index(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.CHAPTERED,
                parts=0,
            )
            project.save()

            folder = root / "capitulos"
            folder.mkdir()

            (folder / "i0010_v001_primeiro.md").touch()
            (folder / "i0020_v001_segundo.md").touch()
            (folder / "i0040_v001_quarto.md").touch()

            project_item = ProjectItem(
                project=project,
                context="capitulos",
            )

            index = ParseNextIndex.parse(project_item)

            assert index == 50

    def test_parse_next_index_empty_folder(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.CHAPTERED,
                parts=0,
            )
            project.save()

            folder = root / "capitulos"
            folder.mkdir()

            project_item = ProjectItem(
                project=project,
                context="capitulos",
            )

            index = ParseNextIndex.parse(project_item)

            assert index == 10

    def test_parse_next_index_ignores_files_without_index(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.CHAPTERED,
                parts=0,
            )
            project.save()

            folder = root / "capitulos"
            folder.mkdir()

            (folder / "i0010_v001_primeiro.md").touch()
            (folder / "resumo.md").touch()
            (folder / ".gitkeep").touch()

            project_item = ProjectItem(
                project=project,
                context="capitulos",
            )

            index = ParseNextIndex.parse(project_item)

            assert index == 20

    def test_standalone_returns_none(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu conto",
                root=root,
                project_type=ProjectType.STANDALONE,
                parts=0,
            )
            project.save()

            project_item = ProjectItem(
                project=project,
            )

            index = ParseNextIndex.parse(project_item)

            assert index is None
