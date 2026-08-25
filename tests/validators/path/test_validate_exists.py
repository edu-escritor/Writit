import pytest

from tests.validators.path.prepare_tests import create_temp_file, get_temp_folder
from validators.path.validate_exists import ValidateExists


def test_validate_existing_path():
    temp_folder = get_temp_folder()
    temp_file = create_temp_file(folder=temp_folder, extension=".tex")

    try:
        result = ValidateExists.validate(temp_file)
        assert result == temp_file
    finally:
        temp_file.unlink(missing_ok=True)


def test_validate_existing_path_nok():
    temp_folder = get_temp_folder()
    temp_file = temp_folder / "nok.tex"

    with pytest.raises(ValueError):
        ValidateExists.validate(temp_file)
