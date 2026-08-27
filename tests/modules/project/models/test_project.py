import tempfile
from pathlib import Path

import pytest

from modules.enums.project_type import ProjectType
from modules.project.models.project import Project


@pytest.fixture(scope="module")
def temp_root() -> Path:
    temp_dir = tempfile.TemporaryDirectory(prefix="writit_test_project_")

    root = Path(temp_dir.name)

    yield root

    temp_dir.cleanup()


def test_save(temp_root: Path):
    project = Project(
        title="Some Nice Project",
        root=temp_root,
        project_type=ProjectType.STANDALONE,
        parts=0,
    )

    project.save()

    assert (temp_root / Project.FILE).is_file()


def test_load(temp_root: Path):
    loaded = Project.load(temp_root)

    assert loaded.title == "Some Nice Project"
    assert loaded.root == temp_root
    assert loaded.project_type == ProjectType.STANDALONE
    assert loaded.parts == 0


def test_empty():
    project = Project.empty()

    assert project.title == "Default"
    assert project.root == Path(tempfile.gettempdir())
    assert project.project_type == ProjectType.STANDALONE
    assert project.parts == 0
