import click

from cli.cli_actions import CliActions


class CliParser:
    @staticmethod
    @click.command(
        help=CliActions.help(),
    )
    @click.argument(
        "module",
        type=click.Choice(CliActions.MODULES),
    )
    @click.argument(
        "action",
        type=click.Choice(CliActions.ACTIONS),
    )
    def cli(module: str, action: str) -> None:
        CliActions.validate_action(
            module=module,
            action=action,
        )