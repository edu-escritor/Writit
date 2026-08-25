from pathlib import Path

import pytest

from validators.validate_not_none import ValidateNotNone


def test_validate_not_none_nok():
    with pytest.raises(ValueError):
        ValidateNotNone.validate(None)


@pytest.mark.parametrize(
    "value",
    (
        "hello",
        "",
        "   ",
        Path("/tmp"),
        Path("."),
        Path("folder/file.txt"),
    ),
)
def test_validate_not_none_ok(value):
    result = ValidateNotNone.validate(value)

    assert result == value


def test_validate_not_none_custom_message():
    message = "The project folder cannot be None!"

    with pytest.raises(ValueError, match=message):
        ValidateNotNone.validate(None, message=message)
