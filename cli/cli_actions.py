from dataclasses import dataclass

import click
from typing import Final

@dataclass(frozen=True)
class CliAction:
    name: str
    description: str


class CliActions:
    # Modules
    MODULE_PROJECT: Final[str] = "project"
    MODULE_FILE: Final[str] = "file"

    MODULES: Final[tuple[str, ...]] = (
        MODULE_PROJECT,
        MODULE_FILE,
    )

    # Project actions
    ACTION_PROJECT_CREATE: Final[str] = "create"
    ACTION_PROJECT_BUILD: Final[str] = "build"
    ACTION_PROJECT_FULL_BUILD: Final[str] = "full-build"
    ACTION_PROJECT_SYNC: Final[str] = "sync"

    # File actions
    ACTION_FILE_CREATE: Final[str] = "create"
    ACTION_FILE_NORMALIZE: Final[str] = "normalize"
    ACTION_FILE_REVISE: Final[str] = "revise"

    ACTIONS: Final[tuple[str, ...]] = (
        ACTION_PROJECT_CREATE,
        ACTION_PROJECT_BUILD,
        ACTION_PROJECT_FULL_BUILD,
        ACTION_PROJECT_SYNC,
        ACTION_FILE_CREATE,
        ACTION_FILE_NORMALIZE,
        ACTION_FILE_REVISE,
    )

    # Action catalog
    project = (
        CliAction(
            ACTION_PROJECT_CREATE,
            "Create a new project.",
        ),
        CliAction(
            ACTION_PROJECT_BUILD,
            "Build the project into a LibreOffice ODT file.",
        ),
        CliAction(
            ACTION_PROJECT_FULL_BUILD,
            "Synchronize the master file and build the project into "
            "a LibreOffice ODT file in a single step.",
        ),
        CliAction(
            ACTION_PROJECT_SYNC,
            "Synchronize the master file with the latest versions "
            "of all project files.",
        ),
    )

    file = (
        CliAction(
            ACTION_FILE_CREATE,
            "Create a new file.",
        ),
        CliAction(
            ACTION_FILE_NORMALIZE,
            "Normalize file names according to the naming convention.",
        ),
        CliAction(
            ACTION_FILE_REVISE,
            "Duplicate the latest version of a file and rename it "
            "to the next revision according to the naming convention.",
        ),
    )

    @staticmethod
    def validate_module(module: str) -> tuple[CliAction, ...]:
        key = module.lower()

        if key not in CliActions.MODULES:
            raise click.BadParameter(
                f"The module '{module}' does not exist!"
            )

        return getattr(CliActions, key)

    @staticmethod
    def validate_action(module: str, action: str) -> CliAction:
        actions = CliActions.validate_module(module)

        for action in actions:
            if action.name == action:
                return action

        raise click.BadParameter(
            f"The action '{action}' does not exist for '{module}'!"
        )

    @staticmethod
    def help() -> str:
        lines: list[str] = [
            "\b",
            "Available modules and actions:",
            "",
        ]

        for module in CliActions.MODULES:
            lines.append(f"{module}:")

            actions = getattr(CliActions, module)

            for action in actions:
                lines.append(
                    f"  {action.name:<12} {action.description}"
                )

            lines.append("")

        return "\n\n".join(lines)