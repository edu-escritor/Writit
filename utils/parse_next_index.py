from modules.enums.project_type import ProjectType
from modules.project.models.project_item import ProjectItem
from utils.parse_index import ParseIndex


class ParseNextIndex:
    @staticmethod
    def parse(project_item: ProjectItem) -> int | None:
        if project_item.project.project_type == ProjectType.STANDALONE:
            return None

        if project_item.context is None:
            raise ValueError("A folder is missing from the project!")

        folder = project_item.project.root / project_item.context

        max_index = 0

        for file in folder.iterdir():
            if not file.is_file():
                continue

            index = ParseIndex().parse(file)

            if index is None:
                continue

            value, _ = index
            max_index = max(max_index, value)

        return max_index
