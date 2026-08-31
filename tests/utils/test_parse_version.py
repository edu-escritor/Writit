import tempfile
from pathlib import Path

from utils.parse_version import ParseVersion


class TestParseVersion:

    def test_parse_version(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "p001_i0010_v006_velho-novo-mundo.md"
            file.touch()

            parser = ParseVersion()

            version = parser.parse(file)

            assert version == (6, 3)

    def test_parse_version_without_version(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "resumo.md"
            file.touch()

            parser = ParseVersion()

            version = parser.parse(file)

            assert version is None

    def test_parse_version_with_different_padding(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "v01_meu-conto.md"
            file.touch()

            parser = ParseVersion()

            version = parser.parse(file)

            assert version == (1, 2)

    def test_directory_returns_none(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            parser = ParseVersion()

            version = parser.parse(root)

            assert version is None
