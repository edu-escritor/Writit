import tempfile
from pathlib import Path

from modules.enums.locales import Locales
from modules.enums.project_type import ProjectType
from modules.file.file_create import FileCreate
from modules.project.models.project import Project


class TestFileCreate:

    def test_create_chapter(self):
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

            service = FileCreate(Locales.PORTUGUESE_EUROPEAN)

            service.execute(
                path=folder,
                title="Primeiro Capítulo",
                part=None,
            )

            created_files = list(folder.glob("*.md"))

            assert len(created_files) == 1

            created_file = created_files[0]

            assert created_file.name.endswith("_v001_primeiro-capitulo.md")
            assert "Primeiro Capítulo" in created_file.read_text(encoding="utf-8")

    def test_create_second_chapter(self):
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

            (folder / "i0010_v001_primeiro-capitulo.md").touch()

            service = FileCreate(Locales.PORTUGUESE_EUROPEAN)

            service.execute(
                path=folder,
                title="Segundo Capítulo",
                part=None,
            )

            created_files = list(folder.glob("*segundo-capitulo.md"))

            assert len(created_files) == 1

    def test_create_in_project_root_raises_error(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            project = Project(
                title="Meu romance",
                root=root,
                project_type=ProjectType.CHAPTERED,
                parts=0,
            )
            project.save()

            service = FileCreate(Locales.PORTUGUESE_EUROPEAN)

            import pytest

            with pytest.raises(
                ValueError,
                match="It's not possible to create a file in the project root!",
            ):
                service.execute(
                    path=root,
                    title="Primeiro Capítulo",
                    part=None,
                )
