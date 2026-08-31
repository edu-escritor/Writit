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

            file = root / "qualquer.md"
            file.touch()

            item = ParseProjectItem.parse(
                path=file,
                title="Meu Conto",
            )

            assert item.project.root == root
            assert item.extension == "md"
            assert item.context == "texto"
            assert item.part is None
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

            file = folder / "i0010_v001_capitulo.md"
            file.touch()

            item = ParseProjectItem.parse(
                path=file,
                title="Primeiro Capítulo",
            )

            assert item.project.root == root
            assert item.extension == "md"
            assert item.context == "capitulos"
            assert item.part is None
            assert item.slug == "primeiro-capitulo"

    def test_parted_with_explicit_part(self):
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

            item = ParseProjectItem.parse(
                path=folder,
                title="Novo Capítulo",
                part=2,
            )

            assert item.project.root == root
            assert item.extension == "md"
            assert item.part == (2, 1)
            assert item.context == "parte_02"
            assert item.slug == "novo-capitulo"

    def test_parted_parses_part_from_file(self):
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

            file = folder / "p001_i0010_v006_velho-novo-mundo.md"
            file.touch()

            item = ParseProjectItem.parse(
                path=file,
                title="Velho Novo Mundo",
            )

            assert item.part == (1, 3)
            assert item.context == "parte_01"
            assert item.slug == "velho-novo-mundo"

    def test_parted_without_part_raises_error(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=3,
            )
            project.save()

            file = root / "arquivo.md"
            file.touch()

            with pytest.raises(
                ValueError,
                match="The project does not contain any part!",
            ):
                ParseProjectItem.parse(
                    path=file,
                    title="Arquivo",
                )

    def test_empty_title_raises_error(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu conto",
                root=root,
                project_type=ProjectType.STANDALONE,
                parts=0,
            )
            project.save()

            file = root / "arquivo.md"
            file.touch()

            with pytest.raises(ValueError):
                ParseProjectItem.parse(
                    path=file,
                    title="",
                )
