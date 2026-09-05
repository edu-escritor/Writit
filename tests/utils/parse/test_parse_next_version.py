import tempfile
from pathlib import Path

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from modules.project.models.project_item import ProjectItem
from utils.parse.parse_next_version import ParseNextVersion


class TestParseNextVersion:

    def test_parse_next_version_with_part_and_index(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=3,
            )
            project.save()

            folder = root / "parte_01"
            folder.mkdir()

            (folder / "p001_i0020_v004_dedicatoria.md").touch()
            (folder / "p001_i0020_v005_sem-perdao.md").touch()
            (folder / "p001_i0020_v011_outro-titulo.md").touch()
            (folder / "p001_i0030_v020_outro.md").touch()

            project_item = ProjectItem(
                project=project,
                context="parte_01",
                part=(1, 3),
                index=(20, 4),
            )

            version = ParseNextVersion.parse(project_item)

            assert version == 12

    def test_parse_next_version_with_index(self):
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

            (folder / "i0020_v004_dedicatoria.md").touch()
            (folder / "i0020_v009_novo-titulo.md").touch()
            (folder / "i0030_v020_outro.md").touch()

            project_item = ProjectItem(
                project=project,
                context="capitulos",
                index=(20, 4),
            )

            version = ParseNextVersion.parse(project_item)

            assert version == 10

    def test_parse_next_version_standalone(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu conto",
                root=root,
                project_type=ProjectType.STANDALONE,
                parts=0,
            )
            project.save()

            folder = root / "texto"
            folder.mkdir()

            (folder / "v004_dedicatoria.md").touch()
            (folder / "v009_sem-perdao.md").touch()
            (folder / "v020_final.md").touch()

            project_item = ProjectItem(
                project=project,
                context="texto",
            )

            version = ParseNextVersion.parse(project_item)

            assert version == 21

    def test_parse_next_version_empty_folder(self):
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
                index=(20, 4),
            )

            version = ParseNextVersion.parse(project_item)

            assert version == 1

    def test_parse_next_version_ignores_other_prefixes(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=3,
            )
            project.save()

            folder = root / "parte_01"
            folder.mkdir()

            (folder / "p001_i0020_v003_primeiro.md").touch()
            (folder / "p001_i0020_v007_segundo.md").touch()
            (folder / "p001_i0030_v050_outro.md").touch()
            (folder / "p002_i0020_v060_outro.md").touch()

            project_item = ProjectItem(
                project=project,
                context="parte_01",
                part=(1, 3),
                index=(20, 4),
            )

            version = ParseNextVersion.parse(project_item)

            assert version == 8
