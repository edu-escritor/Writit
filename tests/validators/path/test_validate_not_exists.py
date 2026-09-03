import pytest

from tests.validators.path.prepare_tests import create_temp_file, get_temp_folder
from validators.path.validate_not_exists import ValidateNotExists


def test_validate_not_existing_path():
    temp_folder = get_temp_folder()
    temp_file = temp_folder / "not_exists.tex"

    temp_file.unlink(missing_ok=True)

    result = ValidateNotExists.validate(temp_file)

    assert result == temp_file


def test_validate_not_existing_path_nok():
    temp_folder = get_temp_folder()
    temp_file = create_temp_file(folder=temp_folder, extension=".tex")

    try:
        with pytest.raises(ValueError):
            ValidateNotExists.validate(temp_file)
    finally:
        temp_file.unlink(missing_ok=True)
