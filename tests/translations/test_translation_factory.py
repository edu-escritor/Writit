from modules.enums.locales import Locales
from translations.english_american import EnglishAmerican
from translations.portuguese_european import PortugueseEuropean
from translations.translation_factory import TranslationFactory


class TestTranslationFactory:

    def test_portuguese_european(self):
        translation = TranslationFactory.get(Locales.PORTUGUESE_EUROPEAN)

        assert translation is PortugueseEuropean

    def test_english_american(self):
        translation = TranslationFactory.get(Locales.ENGLISH_AMERICAN)

        assert translation is EnglishAmerican
