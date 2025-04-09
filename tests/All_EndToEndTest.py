import copy
import os
import re
import sys

from pathlib import Path
from typing import cast
import pytest
import tomlkit

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
@pytest.mark.parametrize(
    "configuration_info",
    [copy.deepcopy(ci) for ci in TestHelpers.ConfigurationInfo.Generate()],
    ids=[ci.name for ci in TestHelpers.ConfigurationInfo.Generate()],
)
def test_All(configuration_info, copie, snapshot) -> None:
    project_dir = TestHelpers.RunTest(copie, configuration_info.configuration)
    assert project_dir is not None

    results: dict[str, str | None] = {}

    for root_str, directories, filenames in os.walk(project_dir):
        root = Path(root_str)
        if root.parts[-1] in [".git", ".venv"]:
            directories[:] = []
            continue

        relative_path = root.relative_to(project_dir)

        if not filenames:
            results[relative_path.as_posix()] = None
            continue

        for filename in filenames:
            if filename == "uv.lock":
                continue

            # Multiple files are populated with dynamic information that is likely to be
            # different between when the test was run and when this code was written. Replace
            # that dynamic information with placeholders that can be used for testing.
            content = (root / filename).read_text(encoding="utf-8")

            for freeform_string in TestHelpers.freeform_strings:
                content = content.replace(
                    configuration_info.configuration[freeform_string], f"<<{freeform_string}>>"
                )

            python_version = ".".join(str(i) for i in sys.version_info[:2])

            if filename == ".copier-answers.yml":
                content = content.replace(str(Path.cwd()), "<<cwd>>")
                content = re.sub(
                    r"^(?P<whitespace>\s+)_commit: .+?$",
                    lambda match: f"{match['whitespace']}_commit: <<commit>>",
                    content,
                    flags=re.MULTILINE,
                )
            elif filename == ".python-version":
                assert content.strip() == python_version, (content, python_version)
                content = "<<python_version>>"
            elif filename == "pyproject.toml":
                toml_content = tomlkit.loads(content)

                project_section = cast(tomlkit.TOMLDocument, toml_content["project"])

                # project.requires-python
                assert project_section["requires-python"] == f">={python_version}", (
                    project_section["requires-python"],
                    python_version,
                )
                project_section["requires-python"] = ">= <<python_version>>"

                # project.authors

                # Note that it is difficult to populate the authors with placeholder values, as this
                # section will not always be present and sections added to the toml will appear at
                # the end of the file. To ensure consistency between those invocations where author
                # is present (and the sections appears in the middle of the file) and those where
                # author is not initially present (where the section would appear at the end of the
                # file when added), we remove the author section entirely.
                project_section.pop("authors", None)

                # dependency-groups.dev
                dependency_group_section = cast(tomlkit.TOMLDocument, toml_content["dependency-groups"])

                dev_dependencies = cast(list, dependency_group_section["dev"])

                # A regex to extract the dependency name and ignore the version information that
                # comes after it.
                dev_dependency_regex = re.compile(r"^(?P<name>\w+).+?")

                versionless_dev_dependencies: list[str] = []

                for dev_dependency in dev_dependencies:
                    match = dev_dependency_regex.match(dev_dependency)
                    assert match, dev_dependency

                    versionless_dev_dependencies.append(match["name"])

                dependency_group_section["dev"] = sorted(versionless_dev_dependencies)

                content = tomlkit.dumps(toml_content)

            results[(relative_path / filename).as_posix()] = content

    assert results == snapshot
