# noqa: D100
import subprocess
import sys
import textwrap

from pathlib import Path
from typing import Annotated

import typer

from typer.core import TyperGroup


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):  # noqa: D101
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs) -> list[str]:  # noqa: ARG002, D102
        return list(self.commands.keys())  # pragma: no cover


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
@app.command("Copy", no_args_is_help=True)
def Copy(
    output_directory: Annotated[
        Path,
        typer.Argument(
            exists=False, file_okay=False, path_type=Path, help="Output directory for the copied project."
        ),  # ty: ignore[no-matching-overload]
    ],
    additional_args: Annotated[
        list[str],
        typer.Argument(help="Additional arguments to pass to copier."),
    ] = [],  # noqa: B006
    skip_uv_version_check: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--skip-uv-version-check", help="Skip checking for the latest version of uv."),
    ] = False,
) -> None:
    """Run copier copy."""

    sys.exit(
        _Execute(
            f"""uv run copier copy "{Path(__file__).parent}" "{output_directory}" --trust {" ".join('"{}"'.format(arg) for arg in additional_args)}""",
            skip_uv_version_check=skip_uv_version_check,
        ),
    )


# ----------------------------------------------------------------------
@app.command("Recopy", no_args_is_help=True)
def Recopy(
    project_directory: Annotated[
        Path,
        typer.Argument(
            exists=True, file_okay=False, path_type=Path, help="Directory for the previously copied project."
        ),  # ty: ignore[no-matching-overload]
    ],
    additional_args: Annotated[
        list[str],
        typer.Argument(help="Additional arguments to pass to copier."),
    ] = [],  # noqa: B006
    skip_uv_version_check: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--skip-uv-version-check", help="Skip checking for the latest version of uv."),
    ] = False,
) -> None:
    """Run copier recopy."""

    sys.exit(
        _Execute(
            f"""uv run copier recopy "{project_directory}" --trust {" ".join('"{}"'.format(arg) for arg in additional_args)}""",
            skip_uv_version_check=skip_uv_version_check,
        ),
    )


# ----------------------------------------------------------------------
@app.command("Update", no_args_is_help=True)
def Update(
    project_directory: Annotated[
        Path,
        typer.Argument(
            exists=True, file_okay=False, path_type=Path, help="Directory for the previously copied project."
        ),  # ty: ignore[no-matching-overload]
    ],
    additional_args: Annotated[
        list[str],
        typer.Argument(help="Additional arguments to pass to copier."),
    ] = [],  # noqa: B006
    skip_uv_version_check: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--skip-uv-version-check", help="Skip checking for the latest version of uv."),
    ] = False,
) -> None:
    """Run copier update."""

    sys.exit(
        _Execute(
            f"""uv run copier update "{project_directory}" --trust {" ".join('"{}"'.format(arg) for arg in additional_args)}""",
            skip_uv_version_check=skip_uv_version_check,
        ),
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _CheckUvVersion() -> bool:
    result = subprocess.run(
        "uv self update --dry-run",  # noqa: S607
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.returncode
    assert result.stderr

    if "Would update uv" in result.stderr:
        sys.stdout.write(
            textwrap.dedent(
                """\
                uv is not currently up-to-date, which may cause problems when using this copier template.
                Please update uv by running "uv self update" or invoke this script with the command line
                argument "--skip-uv-version-check" to skip this check.


                """,
            ),
        )

        return False

    return True


# ----------------------------------------------------------------------
def _Execute(
    command_line: str,
    *,
    skip_uv_version_check: bool,
) -> int:
    if skip_uv_version_check or _CheckUvVersion():
        sys.stdout.write(f"Running: {command_line}...\n\n")

        try:
            subprocess.run(  # noqa: S603
                command_line,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                stdout=sys.stdout,
                check=True,
            )
        except subprocess.CalledProcessError as ex:
            return ex.returncode

    return 0


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()  # pragma: no cover
