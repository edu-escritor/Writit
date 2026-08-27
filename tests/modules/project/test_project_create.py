import tempfile
from pathlib import Path

import pytest

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project
from modules.project.project_create import ProjectCreate


class TestProjectCreate:

    def test_root_does_not_exist(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp) / "does_not_exist"

            service = ProjectCreate()

            with pytest.raises(Exception):
                service.execute(
                    root=root,
                    title="Meu romance",
                    project_type=ProjectType.STANDALONE,
                )

    def test_root_exists(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            service = ProjectCreate()

            service.execute(
                root=root,
                title="Meu romance",
                project_type=ProjectType.STANDALONE,
            )

            project = root / "meu-romance"

            assert project.exists()
            assert project.is_dir()

    def test_project_folder_already_exists(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)
            project = root / "meu-romance"
            project.mkdir()

            service = ProjectCreate()

            with pytest.raises(ValueError, match="The project folder already exists"):
                service.execute(
                    root=root,
                    title="Meu romance",
                    project_type=ProjectType.STANDALONE,
                )

    def test_create_project_successfully(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            service = ProjectCreate()

            service.execute(
                root=root,
                title="Meu romance",
                project_type=ProjectType.PARTED,
                parts=3,
            )

            project = root / "meu-romance"

            assert project.exists()
            assert project.is_dir()

            assert (project / Project.FILE).exists()
            assert (project / Project.FILE).is_file()

            assert (project / "meta").exists()
            assert (project / "meta" / "resumo.md").exists()

            assert (project / "parte_01").exists()
            assert (project / "parte_02").exists()
            assert (project / "parte_03").exists()

            assert (project / "parte_01" / "p001_i0000_parte-01.rst").exists()
            assert (project / "parte_02" / "p002_i0000_parte-02.rst").exists()
            assert (project / "parte_03" / "p003_i0000_parte-03.rst").exists()
