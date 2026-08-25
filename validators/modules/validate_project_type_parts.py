from modules.enums.project_type import ProjectType


class ValidateProjectTypeParts:

    @staticmethod
    def validate(project_type: ProjectType, parts: int | None) -> None:
        ValidateProjectTypeParts.__handle_standalone(project_type, parts)
        ValidateProjectTypeParts.__handle_chaptered(project_type, parts)
        ValidateProjectTypeParts.__handle_parted(project_type, parts)

    @staticmethod
    def __handle_standalone(project_type: ProjectType, parts: int | None) -> None:
        if project_type != ProjectType.STANDALONE:
            return None

        if parts is not None and parts > 0:
            raise ValueError("A standalone project cannot have any parts!")

        return None

    @staticmethod
    def __handle_chaptered(project_type: ProjectType, parts: int | None) -> None:
        if project_type != ProjectType.CHAPTERED:
            return None

        if parts is not None and parts > 0:
            raise ValueError(
                "A chaptered project cannot have any parts! Change it to parted."
            )

        return None

    @staticmethod
    def __handle_parted(project_type: ProjectType, parts: int | None) -> None:
        if project_type != ProjectType.PARTED:
            return None

        if parts is None or parts < 1:
            raise ValueError(
                "A parted project needs at least one part! Change it to chaptered."
            )

        return None
