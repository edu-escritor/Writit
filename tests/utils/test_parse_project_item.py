import tempfile
from pathlib import Path

import pytest

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from utils.parse_project_item import ParseProjectItem


class TestParseItem:

    def test_standalone(self):
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

            file = folder / "v004_meu-conto.md"
            file.touch()

            item = ParseProjectItem.parse(file)

            assert item.project.root == root
            assert item.extension == "md"
            assert item.context == "texto"
            assert item.part is None
            assert item.index is None
            assert item.version == (4, 3)
            assert item.slug == "meu-conto"

    def test_chaptered(self):
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

            file = folder / "i0010_v001_primeiro-capitulo.md"
            file.touch()

            item = ParseProjectItem.parse(file)

            assert item.project.root == root
            assert item.extension == "md"
            assert item.context == "capitulos"
            assert item.part is None
            assert item.index == (10, 4)
            assert item.version == (1, 3)
            assert item.slug == "primeiro-capitulo"

    def test_parted(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=3,
            )
            project.save()

            folder = root / "parte_02"
            folder.mkdir()

            file = folder / "p002_i0010_v006_velho-novo-mundo.md"
            file.touch()

            item = ParseProjectItem.parse(file)

            assert item.project.root == root
            assert item.extension == "md"
            assert item.context == "parte_02"
            assert item.part == (2, 3)
            assert item.index == (10, 4)
            assert item.version == (6, 3)
            assert item.slug == "velho-novo-mundo"

    def test_different_extension(self):
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

            file = folder / "i0020_v012_outro-capitulo.rst"
            file.touch()

            item = ParseProjectItem.parse(file)

            assert item.extension == "rst"
            assert item.index == (20, 4)
            assert item.version == (12, 3)
            assert item.slug == "outro-capitulo"

    def test_invalid_slug_without_separator(self):
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

            file = folder / "v001.md"
            file.touch()

            with pytest.raises(ValueError):
                ParseProjectItem.parse(file)

    def test_invalid_empty_slug(self):
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

            file = folder / "v001_.md"
            file.touch()

            with pytest.raises(ValueError):
                ParseProjectItem.parse(file)

    def test_directory_raises_error(self):
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

            with pytest.raises(ValueError):
                ParseProjectItem.parse(folder)
