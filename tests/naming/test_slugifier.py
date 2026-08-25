import pytest

from naming.slugifier import Slugifier


@pytest.mark.parametrize("separator", ["-", "_"])
def test_ok_separators(separator: str):
    good = f"this{separator}is{separator}good"
    bad = "This Is GOOD"

    result = Slugifier.slugify(bad, separator=separator)

    assert result == good


def test_ok_lowercase():
    good = "this-is-good"
    bad = "This Is GOOD"

    result = Slugifier.slugify(bad, lowercase=True)

    assert result == good


def test_ok_uppercase():
    good = "THIS-IS-GOOD"
    bad = "This Is GOOD"

    result = Slugifier.slugify(bad, lowercase=False)

    assert result == good


def test_default_values():
    result = Slugifier.slugify("Hello Beautiful World")

    assert result == "hello-beautiful-world"


def test_remove_accents():
    result = Slugifier.slugify("Olá Número Coração")

    assert result == "ola-numero-coracao"


def test_multiple_spaces():
    result = Slugifier.slugify("Hello       Beautiful     World")

    assert result == "hello-beautiful-world"


def test_leading_and_trailing_spaces():
    result = Slugifier.slugify("    Hello World    ")

    assert result == "hello-world"


def test_max_length():
    result = Slugifier.slugify(
        "Hello Beautiful World",
        max_length=15
    )

    assert len(result) <= 15


def test_empty_string():
    result = Slugifier.slugify("")

    assert result == ""


def test_only_spaces():
    result = Slugifier.slugify("       ")

    assert result == ""


def test_only_punctuation():
    result = Slugifier.slugify("... !!! ???")

    assert result == ""


def test_numbers():
    result = Slugifier.slugify("Chapter 23")

    assert result == "chapter-23"


def test_special_characters():
    result = Slugifier.slugify("Number #$%&23")

    assert result == "number-23"