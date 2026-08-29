import tempfile
from pathlib import Path

import pytest

from modules.enums.project_type import ProjectType
from modules.project.project_add_part import ProjectAddPart
from modules.project.project_create import ProjectCreate


class TestProjectAddPart:

    def test_add_part_successfully(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            create = ProjectCreate()
            create.execute(
                root=root,
                title="Meu romance",
                project_type=ProjectType.PARTED,
                parts=3,
            )

            project_root = root / "meu-romance"

            service = ProjectAddPart()
            service.execute(project_root)

            assert (project_root / "parte_04").exists()
            assert (project_root / "parte_04").is_dir()

            assert (project_root / "parte_04" / "p004_i0000_parte-04.rst").is_file()

    def test_add_part_to_non_parted_project(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            create = ProjectCreate()
            create.execute(
                root=root,
                title="Meu romance",
                project_type=ProjectType.STANDALONE,
            )

            project_root = root / "meu-romance"

            service = ProjectAddPart()

            with pytest.raises(
                ValueError,
                match="The project does not have parts!",
            ):
                service.execute(project_root)

    def test_add_part_preserves_existing_parts(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            create = ProjectCreate()
            create.execute(
                root=root,
                title="Meu romance",
                project_type=ProjectType.PARTED,
                parts=2,
            )

            project_root = root / "meu-romance"

            service = ProjectAddPart()
            service.execute(project_root)

            assert (project_root / "parte_01").is_dir()
            assert (project_root / "parte_02").is_dir()
            assert (project_root / "parte_03").is_dir()
