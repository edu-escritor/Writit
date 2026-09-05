import tempfile
from pathlib import Path

import pytest

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from utils.parse.parse_root import ParseRoot


class TestParseRoot:

    def test_parse_root_from_root(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.STANDALONE,
                parts=0,
            )
            project.save()

            parser = ParseRoot()

            parsed_root = parser.parse(root)

            assert parsed_root == root

    def test_parse_root_from_subfolder(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=1,
            )
            project.save()

            folder = root / "parte_01"
            folder.mkdir()

            parser = ParseRoot()

            parsed_root = parser.parse(folder)

            assert parsed_root == root

    def test_parse_root_from_file(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=1,
            )
            project.save()

            folder = root / "parte_01"
            folder.mkdir()

            file = folder / "p001_i0010_v006_capitulo.md"
            file.touch()

            parser = ParseRoot()

            parsed_root = parser.parse(file)

            assert parsed_root == root

    def test_parse_root_from_nested_subfolder(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=1,
            )
            project.save()

            nested = root / "parte_01" / "subfolder"
            nested.mkdir(parents=True)

            parser = ParseRoot()

            parsed_root = parser.parse(nested)

            assert parsed_root == root

    def test_invalid_project_root(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            parser = ParseRoot()

            with pytest.raises(
                ValueError,
                match="is not a valid project root!",
            ):
                parser.parse(root)
