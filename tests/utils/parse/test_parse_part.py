import tempfile
from pathlib import Path

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from utils.parse.parse_part import ParsePart


class TestParsePart:

    def test_parse_part_from_file(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=3,
            )
            project.save()

            file = root / "p001_i0010_v006_velho-novo-mundo.md"
            file.touch()

            parser = ParsePart()

            part = parser.parse(file)

            assert part == (1, 3)

    def test_parse_part_without_part(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=3,
            )
            project.save()

            file = root / "i0010_v006_velho-novo-mundo.md"
            file.touch()

            parser = ParsePart()

            part = parser.parse(file)

            assert part is None

    def test_parse_part_with_different_padding(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.PARTED,
                parts=10,
            )
            project.save()

            file = root / "p01_i0010_v006_velho-novo-mundo.md"
            file.touch()

            parser = ParsePart()

            part = parser.parse(file)

            assert part == (1, 2)

    def test_parse_part_from_portuguese_folder(self):
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

            parser = ParsePart()

            part = parser.parse(folder)

            assert part == (1, 2)

    def test_parse_part_from_english_folder(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="My novel",
                root=root,
                project_type=ProjectType.PARTED,
                parts=3,
            )
            project.save()

            folder = root / "part_01"
            folder.mkdir()

            parser = ParsePart()

            part = parser.parse(folder)

            assert part == (1, 2)
