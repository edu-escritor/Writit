from pathlib import Path

from naming.slugifier import Slugifier
from validators.path.validate_exists import ValidateExists
from validators.path.validate_is_file import ValidateIsFile


class ParseSlug:

    # noinspection PyMethodMayBeStatic
    def parse(self, path: str | Path, title: str | None) -> str:
        path = ValidateExists.validate(path)
        path = ValidateIsFile.validate(path)

        if title is not None:
            return Slugifier.slugify(title)

        stem = path.stem
        if "_" not in stem:
            raise ValueError(f"Invalid file name: {path.name}")

        _, slug = stem.rsplit("_", 1)

        if not slug:
            raise ValueError(f"Invalid file name: {path.name}")

        return slug
