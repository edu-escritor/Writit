from pathlib import Path

import click

from modules.enums.locales import Locales
from modules.enums.project_type import ProjectType
from modules.file.file_create import FileCreate
from modules.project.project_add_part import ProjectAddPart
from modules.project.project_create import ProjectCreate


@click.group()
@click.option(
    "--locale",
    type=click.Choice([locale.value for locale in Locales]),
    default=Locales.PORTUGUESE_EUROPEAN.value,
    show_default=True,
)
@click.pass_context
def cli(ctx: click.Context, locale: str) -> None:
    ctx.ensure_object(dict)
    ctx.obj["locale"] = Locales(locale)


@cli.group()
def project() -> None:
    pass


@project.command("create")
@click.argument(
    "root",
    type=click.Path(path_type=Path),
)
@click.option(
    "--title",
    "-t",
    type=str,
    required=True,
)
@click.option(
    "--project-type",
    type=click.Choice([project_type.value for project_type in ProjectType]),
    default=ProjectType.STANDALONE.value,
)
@click.option(
    "--parts",
    "-p",
    type=int,
    default=0,
)
@click.pass_context
def project_create(
    ctx: click.Context,
    root: Path,
    title: str,
    project_type: str,
    parts: int,
) -> None:
    locale = Locales(ctx.obj["locale"])
    ProjectCreate(locale).execute(root=root, title=title, project_type=ProjectType(project_type), parts=parts)


@project.command("add-part")
@click.argument(
    "root",
    type=click.Path(path_type=Path),
)
def project_add_part(ctx: click.Context, root: Path) -> None:
    locale = Locales(ctx.obj["locale"])
    ProjectAddPart(locale).execute(root=root)


@cli.group()
def file() -> None:
    pass


@file.command("create")
@click.argument(
    "path",
    type=click.Path(path_type=Path),
)
@click.option(
    "--title",
    "-t",
    type=str,
    required=True,
)
@click.option(
    "--part",
    "-p",
    type=int,
    default=None,
)
def file_create(
    path: Path,
    title: str,
    part: int | None,
) -> None:
    FileCreate().execute(
        path=path,
        title=title,
        part=part,
    )


if __name__ == "__main__":
    cli()
