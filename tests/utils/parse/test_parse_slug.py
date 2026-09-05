import tempfile
from pathlib import Path

import pytest

from utils.parse.parse_slug import ParseSlug


class TestParseSlug:

    def test_parse_slug_from_file(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "p001_i0010_v004_velho-novo-mundo.rst"
            file.touch()

            slug = ParseSlug().parse(file, None)

            assert slug == "velho-novo-mundo"

    def test_parse_slug_without_part(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "i0010_v004_velho-novo-mundo.rst"
            file.touch()

            slug = ParseSlug().parse(file, None)

            assert slug == "velho-novo-mundo"

    def test_parse_slug_without_prefix(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "v004_velho-novo-mundo.rst"
            file.touch()

            slug = ParseSlug().parse(file, None)

            assert slug == "velho-novo-mundo"

    def test_parse_slug_from_title(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "v004_velho-novo-mundo.rst"
            file.touch()

            slug = ParseSlug().parse(file, "Um Novo Mundo")

            assert slug == "novo-mundo"

    def test_parse_slug_without_separator(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "velho-novo-mundo.rst"
            file.touch()

            with pytest.raises(ValueError):
                ParseSlug().parse(file, None)

    def test_parse_slug_empty(self):
        with tempfile.TemporaryDirectory(prefix="writit_test_") as temp:
            root = Path(temp)

            file = root / "v004_.rst"
            file.touch()

            with pytest.raises(ValueError):
                ParseSlug().parse(file, None)
