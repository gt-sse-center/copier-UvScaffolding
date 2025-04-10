import shutil

from pathlib import Path
from typing import Annotated

import typer

from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from typer.core import TyperGroup

import TestHelpers


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):
    # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.commands.keys()


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
@app.command("EntryPoint", no_args_is_help=True)
def EntryPoint(
    output_dir: Annotated[
        Path,
        typer.Argument(
            file_okay=False, resolve_path=True, help="The directory where output will be written."
        ),
    ],
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    """Generates all permutations of the templates to an output directory. Doing this makes it easier to validate the output of each configuration."""

    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        template_dir = Path(__file__).parent.parent

        for configuration_info in TestHelpers.ConfigurationInfo.Generate():
            with dm.Nested(f"Generating '{configuration_info.name}'...", suffix="\n") as this_dm:
                this_output_dir = output_dir / configuration_info.name

                TestHelpers.RunManually(
                    this_dm,
                    template_dir,
                    this_output_dir,
                    configuration_info.configuration,
                )

                if this_dm.result == 0:
                    for remove_dir in [".git", ".venv"]:
                        this_remove_dir = this_output_dir / remove_dir

                        if this_remove_dir.is_dir():
                            shutil.rmtree(this_remove_dir)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()
