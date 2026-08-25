import pytest

from naming.rules.remove_punctuation_marks import RemovePunctuationMarks


@pytest.mark.parametrize(
    "mark",
    RemovePunctuationMarks.PUNCTUATION
)
def test_remove_punctuation_marks(mark):
    good = "Hello world"
    bad = f"{mark}Hello{mark} world{mark}"

    result = RemovePunctuationMarks().apply(bad)

    assert result == good