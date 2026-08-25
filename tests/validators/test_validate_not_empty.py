import pytest

from validators.validate_not_empty import ValidateNotEmpty


@pytest.mark.parametrize(
    "value",
    (
        None,
        "",
        " ",
        "   ",
        "\t",
        "\n",
        "\r\n",
        " \t \n ",
    ),
)
def test_validate_not_empty_nok(value):
    with pytest.raises(ValueError):
        ValidateNotEmpty.validate(value)


@pytest.mark.parametrize(
    "value, expected",
    (
        ("hello", "hello"),
        (" hello", "hello"),
        ("hello ", "hello"),
        ("  hello  ", "hello"),
        ("\thello\t", "hello"),
        ("\nhello\n", "hello"),
        (" \t hello world \n ", "hello world"),
    ),
)
def test_validate_not_empty_ok(value, expected):
    result = ValidateNotEmpty.validate(value)

    assert result == expected


def test_validate_not_empty_custom_message():
    message = "The title cannot be empty!"

    with pytest.raises(ValueError, match=message):
        ValidateNotEmpty.validate("   ", message=message)
