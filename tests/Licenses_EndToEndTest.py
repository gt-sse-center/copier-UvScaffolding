import copy

from pathlib import Path
from typing import Any

import pytest
import tomlkit

from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from dbrownell_Common.Streams.StreamDecorator import StreamDecorator

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_LicenseToNone(copie) -> None:
    """Tests the scenario where a license is selected during the initial call to copy and then set to None on a second call to copy in the same output directory."""

    none_configuration, not_none_configuration = _GetConfigurations()

    # Run the not_none_configuration
    output_dir = TestHelpers.RunTest(copie, not_none_configuration.configuration)
    assert output_dir is not None

    assert (output_dir / "LICENSE").is_file()

    pyproject_content = _LoadPyproject(output_dir)
    assert "license" in pyproject_content["project"]

    # Run the none_configuration
    with DoneManager.Create(StreamDecorator(None), "") as dm:
        TestHelpers.RunManually(
            dm,
            Path.cwd(),
            output_dir,
            none_configuration.configuration,
        )

    assert not (output_dir / "LICENSE").exists()

    pyproject_content = _LoadPyproject(output_dir)
    assert "license" not in pyproject_content["project"]


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_NoneToLicense(copie) -> None:
    """Tests the scenario where a license is set to None during the initial call to copy and then set to a license on a second call to copy in the same output directory."""

    none_configuration, not_none_configuration = _GetConfigurations()

    # Run the none_configuration
    output_dir = TestHelpers.RunTest(copie, none_configuration.configuration)
    assert output_dir is not None

    assert not (output_dir / "LICENSE").exists()

    pyproject_content = _LoadPyproject(output_dir)
    assert "license" not in pyproject_content["project"]

    # Run the not_none_configuration
    with DoneManager.Create(StreamDecorator(None), "") as dm:
        TestHelpers.RunManually(
            dm,
            Path.cwd(),
            output_dir,
            not_none_configuration.configuration,
        )

    assert (output_dir / "LICENSE").is_file()

    pyproject_content = _LoadPyproject(output_dir)
    assert "license" in pyproject_content["project"]


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _LoadPyproject(project_dir: Path) -> dict[str, Any]:
    pyproject_path = project_dir / "pyproject.toml"
    assert pyproject_path.is_file(), pyproject_path

    with pyproject_path.open("r", encoding="utf-8") as f:
        content = tomlkit.load(f)

    return content


# ----------------------------------------------------------------------
def _GetConfigurations() -> tuple[TestHelpers.ConfigurationInfo, TestHelpers.ConfigurationInfo]:
    none_configuration: TestHelpers.ConfigurationInfo | None = None
    not_none_configuration: TestHelpers.ConfigurationInfo | None = None

    for configuration in TestHelpers.ConfigurationInfo.Generate():
        if none_configuration is None:
            assert configuration.name == "None"
            none_configuration = copy.deepcopy(configuration)
        elif not_none_configuration is None:
            assert configuration.name != "None"
            not_none_configuration = copy.deepcopy(configuration)

            break
        else:
            assert False

    assert none_configuration is not None
    assert not_none_configuration is not None

    return none_configuration, not_none_configuration
