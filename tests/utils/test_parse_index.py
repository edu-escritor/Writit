import tempfile
from pathlib import Path

from utils.parse_index import ParseIndex


class TestParseIndex:

    def test_parse_index(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "p001_i0010_v006_velho-novo-mundo.md"
            file.touch()

            parser = ParseIndex()

            index = parser.parse(file)

            assert index == (10, 4)

    def test_parse_index_without_index(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "v006_velho-novo-mundo.md"
            file.touch()

            parser = ParseIndex()

            index = parser.parse(file)

            assert index is None

    def test_parse_index_with_different_padding(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "i010_capitulo.md"
            file.touch()

            parser = ParseIndex()

            index = parser.parse(file)

            assert index == (10, 3)

    def test_directory_returns_none(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            parser = ParseIndex()

            index = parser.parse(root)

            assert index is None
