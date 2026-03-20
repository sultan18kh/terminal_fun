"""CLI entry point for terminal_fun. Run with: python -m terminal_fun"""

import typer

from terminal_fun.tools import eid_mubarak as _eid_mubarak_mod

app = typer.Typer(
    name="terminal_fun",
    help="A collection of fun, visually striking terminal-based tools and animations.",
    no_args_is_help=True,
)

eid_app = typer.Typer(help="Animated Eid Mubarak terminal greeting.")


@eid_app.callback(invoke_without_command=True)
def eid_mubarak(
    static: bool = typer.Option(False, "--static", "-s", help="Skip animation, print final frame instantly."),
    theme: str = typer.Option("classic", "--theme", "-t", help="Color theme: classic, royal, or minimal."),
) -> None:
    """Animated Eid Mubarak terminal greeting."""
    _eid_mubarak_mod.run(static=static, theme=theme)


app.add_typer(eid_app, name="eid-mubarak")

if __name__ == "__main__":
    app()
