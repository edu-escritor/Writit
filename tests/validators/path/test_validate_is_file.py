import pytest

from tests.validators.path.prepare_tests import create_temp_file, get_temp_folder
from validators.path.validate_is_file import ValidateIsFile


def test_validate_is_file():
    temp_folder = get_temp_folder()
    temp_file = create_temp_file(folder=temp_folder, extension=".tex")

    try:
        result = ValidateIsFile.validate(temp_file)

        assert result == temp_file
    finally:
        temp_file.unlink(missing_ok=True)


def test_validate_is_file_nok():
    temp_folder = get_temp_folder()

    with pytest.raises(ValueError):
        ValidateIsFile.validate(temp_folder)
