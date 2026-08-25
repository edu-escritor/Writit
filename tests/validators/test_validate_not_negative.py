import pytest

from validators.validate_not_negative import ValidateNotNegative


@pytest.mark.parametrize(
    "value",
    (
        -1,
        -10,
        -100,
    ),
)
def test_validate_not_negative_nok(value):
    with pytest.raises(ValueError):
        ValidateNotNegative.validate(value)


@pytest.mark.parametrize(
    "value",
    (
        0,
        1,
        10,
        100,
    ),
)
def test_validate_not_negative_ok(value):
    result = ValidateNotNegative.validate(value)

    assert result == value


def test_validate_not_negative_custom_message():
    message = "The number of parts cannot be negative!"

    with pytest.raises(ValueError, match=message):
        ValidateNotNegative.validate(-1, message=message)
