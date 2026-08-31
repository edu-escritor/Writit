import re
from pathlib import Path

from validators.path.validate_exists import ValidateExists


class ParseIndex:

    # noinspection PyMethodMayBeStatic
    def parse(self, path: str | Path) -> tuple[int, int] | None:
        path = ValidateExists.validate(path)

        if path.is_dir():
            return None

        match = re.search(r"(?:^|_)i(\d+)(?:_|$)", path.name)

        if match:
            raw_index = match.group(1)

            return (
                int(raw_index),
                len(raw_index),
            )

        return None
