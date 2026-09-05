import re
from pathlib import Path

from utils.parse.parse_index import ParseIndex
from utils.parse.parse_part import ParsePart
from validators.path.validate_exists import ValidateExists
from validators.path.validate_is_file import ValidateIsFile


class FileTitleHandler:

    @staticmethod
    def handle(path: str | Path) -> str:
        path = ValidateIsFile.validate(path)
        path = ValidateExists.validate(path)

        level_increment = FileTitleHandler.__fetch_level_increment(path)

        lines = path.read_text(encoding="utf-8").splitlines()

        while lines and not lines[0].strip():
            lines.pop(0)

        while lines and not lines[-1].strip():
            lines.pop()

        content: list[str] = []

        for line in lines:
            content.append(
                FileTitleHandler.__increase_header_level(
                    line=line,
                    increment=level_increment,
                )
            )

        return "\n".join(content)

    @staticmethod
    def __fetch_level_increment(path: Path) -> int:
        part = ParsePart().parse(path)
        index = ParseIndex().parse(path)

        # Standalone text or chapter without part
        if part is None:
            return 1

        # Part title
        if index is not None and index[0] == 0:
            return 1

        # Chapter inside a part
        return 2

    @staticmethod
    def __increase_header_level(line: str, increment: int) -> str:
        stripped = line.strip()

        match = re.match(r"^(#{1,6})\s+(.+)$", stripped)

        if match is None:
            return line

        header = match.group(1)
        title = match.group(2)

        new_header = "#" * (len(header) + increment)

        return f"{new_header} {title}"
