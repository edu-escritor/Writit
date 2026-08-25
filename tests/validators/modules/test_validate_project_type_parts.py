import pytest

from modules.enums.project_type import ProjectType
from validators.modules.validate_project_type_parts import ValidateProjectTypeParts


@pytest.mark.parametrize(
    "project_type, parts",
    (
        (ProjectType.STANDALONE, None),
        (ProjectType.STANDALONE, 0),
        (ProjectType.CHAPTERED, None),
        (ProjectType.CHAPTERED, 0),
        (ProjectType.PARTED, 1),
        (ProjectType.PARTED, 2),
        (ProjectType.PARTED, 10),
    ),
)
def test_validate_project_type_parts_ok(project_type, parts):
    ValidateProjectTypeParts.validate(
        project_type=project_type,
        parts=parts,
    )


@pytest.mark.parametrize(
    "project_type, parts",
    (
        (ProjectType.STANDALONE, 1),
        (ProjectType.STANDALONE, 2),
        (ProjectType.CHAPTERED, 1),
        (ProjectType.CHAPTERED, 2),
        (ProjectType.PARTED, None),
        (ProjectType.PARTED, 0),
    ),
)
def test_validate_project_type_parts_nok(project_type, parts):
    with pytest.raises(ValueError):
        ValidateProjectTypeParts.validate(
            project_type=project_type,
            parts=parts,
        )
