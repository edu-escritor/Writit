import re
from pathlib import Path

from validators.path.validate_exists import ValidateExists


class ParseVersion:

    # noinspection PyMethodMayBeStatic
    def parse(self, path: str | Path) -> tuple[int, int] | None:
        path = ValidateExists.validate(path)

        if path.is_dir():
            return None

        match = re.search(r"(?:^|_)v(\d+)(?:_|$)", path.name)

        if match:
            raw_version = match.group(1)

            return (
                int(raw_version),
                len(raw_version),
            )

        return None
