import pytest

from tests.validators.path.prepare_tests import create_temp_file, get_temp_folder
from validators.path.validate_is_dir import ValidateIsDir


def test_validate_is_dir():
    temp_folder = get_temp_folder()

    result = ValidateIsDir.validate(temp_folder)

    assert result == temp_folder


def test_validate_is_dir_nok():
    temp_folder = get_temp_folder()
    temp_file = create_temp_file(folder=temp_folder, extension=".tex")

    try:
        with pytest.raises(ValueError):
            ValidateIsDir.validate(temp_file)
    finally:
        temp_file.unlink(missing_ok=True)
