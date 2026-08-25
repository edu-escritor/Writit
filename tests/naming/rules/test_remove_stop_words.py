import pytest

from naming.rules.remove_stop_words import RemoveStopWords


@pytest.mark.parametrize(
    "word",
    RemoveStopWords.STOP_WORDS_EN
)
def test_remove_stop_words_en(word):
    good = "Hello world"
    bad = f"{word} Hello {word} world {word}"

    result = RemoveStopWords().apply(bad)

    assert result == good

def test_remove_stop_words_en_repeated():
    good = "This is world"
    bad = "This is the the world"

    result = RemoveStopWords().apply(bad)

    assert result == good

@pytest.mark.parametrize(
    "word",
    RemoveStopWords.STOP_WORDS_PT
)
def test_remove_stop_words_pt(word):
    good = "Olá mundo"
    bad = f"{word} Olá {word} mundo {word}"

    result = RemoveStopWords().apply(bad)

    assert result == good

def test_remove_stop_words_pt_repeated():
    good = "Este é mundo"
    bad = "Este é o o mundo"

    result = RemoveStopWords().apply(bad)

    assert result == good