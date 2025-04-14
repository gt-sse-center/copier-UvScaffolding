import uuid

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator

import rtyaml
import tomlkit

from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx
from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common import SubprocessEx


# ----------------------------------------------------------------------
# copier values that can be any string value.
freeform_strings: list[str] = [
    "author_name",
    "author_email",
    "github_username",
    "github_repo_name",
]


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class ConfigurationInfo:
    """Information about a single configuration."""

    # ----------------------------------------------------------------------
    name: str
    configuration: dict[str, Any]
    is_valid: bool = field(kw_only=True, default=True)

    # ----------------------------------------------------------------------
    @classmethod
    def Generate(
        cls,
        *,
        include_invalid: bool = False,
    ) -> Generator["ConfigurationInfo", None, None]:
        yield from _EnumerateConfigurations(include_invalid=include_invalid)


# ----------------------------------------------------------------------
def RunTest(
    copie: Any,
    configuration: dict[str, Any],
    *,
    expect_failure: bool = False,
) -> Path | None:
    result = copie.copy(extra_answers=configuration)

    if expect_failure:
        assert result.exit_code != 0, result.exit_code
        assert result.exception is not None
        return None

    assert result.exit_code == 0, result
    assert result.exception is None, result.exception
    assert result.project_dir.is_dir(), result.project_dir

    return result.project_dir


# ----------------------------------------------------------------------
def RunManually(
    dm: DoneManager,
    template_dir: Path,
    output_dir: Path,
    configuration: dict[str, Any],
) -> None:
    configuration_filename = PathEx.CreateTempFileName(".yaml")

    with configuration_filename.open("w") as f:
        rtyaml.dump(configuration, f)

    with ExitStack(configuration_filename.unlink):
        command_line = f'copier copy "{template_dir}" "{output_dir}" --trust --overwrite --defaults --data-file "{configuration_filename}" --vcs-ref=HEAD'

        dm.WriteVerbose(f"Command line: {command_line}\n\n")

        with dm.YieldStream() as stream:
            dm.result = SubprocessEx.Stream(command_line, stream)


# ----------------------------------------------------------------------
def LoadPyproject(project_dir: Path) -> dict[str, Any]:
    pyproject_path = project_dir / "pyproject.toml"
    assert pyproject_path.is_file(), pyproject_path

    with pyproject_path.open("r", encoding="utf-8") as f:
        content = tomlkit.load(f)

    return content


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _EnumerateConfigurations(
    *,
    include_invalid: bool,
) -> Generator[ConfigurationInfo, None, None]:
    configuration: dict[str, Any] = {}

    for freeform_string in freeform_strings:
        configuration[freeform_string] = str(uuid.uuid4()).upper().replace("-", "")

    # Do not make the project name random, as it needs to remain consistent across invocations
    # for valid comparisons (for example, when the name is used to create directories).
    configuration["project_name"] = "this_is_the_project_name"
    configuration["python_package_name"] = configuration["project_name"]

    name_parts: list[str] = []

    for license_value in [
        "None",
        "Apache-2.0",
        "BSD-3-Clause-Clear",
        "BSL-1.0",
        "GPL-3.0-or-later",
        "MIT",
    ]:
        configuration["license"] = license_value

        name_parts.append(license_value)
        with ExitStack(name_parts.pop):
            yield ConfigurationInfo("-".join(name_parts), configuration)
