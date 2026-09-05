from modules.project.models.project_item import ProjectItem
from utils.parse.parse_version import ParseVersion


class ParseNextVersion:

    @staticmethod
    def parse(project_item: ProjectItem) -> int:
        if project_item.context is None:
            raise ValueError("A folder is missing from the project!")

        folder = project_item.project.root / project_item.context
        prefix = project_item.prefix

        max_version = 0

        for file in folder.iterdir():
            if not file.is_file():
                continue

            if prefix:
                expected_prefix = f"{prefix}_"

                if not file.name.startswith(expected_prefix):
                    continue

            version = ParseVersion().parse(file)

            if version is None:
                continue

            value, _ = version
            max_version = max(max_version, value)

        return max_version + 1
