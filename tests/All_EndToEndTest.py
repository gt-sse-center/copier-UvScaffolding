import copy
import os
import re

from pathlib import Path

import pytest

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

    for root_str, _, filenames in os.walk(project_dir):
        root = Path(root_str)
        relative_path = root.relative_to(project_dir)

        if not filenames:
            results[relative_path.as_posix()] = None
            continue

        for filename in filenames:
            content = (root / filename).read_text(encoding="utf-8")

            for freeform_string in TestHelpers.freeform_strings:
                content = content.replace(
                    configuration_info.configuration[freeform_string], f"<<{freeform_string}>>"
                )

            if filename == ".copier-answers.yml":
                content = content.replace(str(Path.cwd()), "<<cwd>>")
                content = re.sub(
                    r"^(?P<whitespace>\s+)_commit: .+?$",
                    lambda match: f"{match['whitespace']}_commit: <<commit>>",
                    content,
                    flags=re.MULTILINE,
                )
            results[(relative_path / filename).as_posix()] = content

    assert results == snapshot
