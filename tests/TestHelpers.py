import uuid

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator


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

    # We will generate more ConfigurationInfo instances in future commits
    yield ConfigurationInfo("", configuration)
