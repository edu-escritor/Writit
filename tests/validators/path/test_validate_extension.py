import pytest

from tests.validators.path.prepare_tests import create_temp_file, get_temp_folder
from validators.path.validate_extension import ValidateExtension


@pytest.mark.parametrize(
    "extension",
    ValidateExtension.VALID_EXTENSIONS,
)
def test_validate_extension(extension: str):
    temp_folder = get_temp_folder()
    temp_file = create_temp_file(
        folder=temp_folder,
        extension=extension,
    )

    try:
        result = ValidateExtension.validate(temp_file)

        assert result == temp_file
    finally:
        temp_file.unlink(missing_ok=True)


def test_validate_extension_nok():
    temp_folder = get_temp_folder()
    temp_file = create_temp_file(folder=temp_folder, extension=".txt")

    try:
        with pytest.raises(ValueError):
            ValidateExtension.validate(temp_file)
    finally:
        temp_file.unlink(missing_ok=True)
