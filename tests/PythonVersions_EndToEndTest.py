from pathlib import Path

import pytest

from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.Streams.StreamDecorator import StreamDecorator

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_ChangePythonVersionsPyProject(copie) -> None:
    """Tests that pyproject.toml file is updated when python versions change."""

    configuration = next(TestHelpers.ConfigurationInfo.Generate()).configuration

    # Generate with the default classifiers
    output_dir = TestHelpers.RunTest(copie, configuration)
    assert output_dir is not None

    original_project = TestHelpers.LoadPyproject(output_dir)["project"]

    original_classifiers = _GetPythonVersionClassifiers(original_project["classifiers"])
    assert original_classifiers

    # Generate with new classifiers
    new_versions: list[str] = ["1.2", "2.3", "2.10"]
    configuration["python_versions"] = ", ".join(new_versions)

    with DoneManager.Create(StreamDecorator(None), "") as dm:
        TestHelpers.RunManually(
            dm,
            Path.cwd(),
            output_dir,
            configuration,
        )

    new_project = TestHelpers.LoadPyproject(output_dir)["project"]

    new_classifiers = _GetPythonVersionClassifiers(new_project["classifiers"])
    assert all(new_version in new_classifiers for new_version in new_versions), (
        new_classifiers,
        new_versions,
    )
    assert len(new_classifiers) == len(new_versions), (new_classifiers, new_versions)

    # Test to see that `requires-python` has been updated
    assert new_project["requires-python"] != original_project["requires-python"]
    assert new_versions[0] in new_project["requires-python"], (
        new_versions[0],
        new_project["requires-python"],
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetPythonVersionClassifiers(classifiers: list[str]) -> list[str]:
    """Extracts the Python version classifiers from the provided list of classifiers."""

    prefix = "Programming Language :: Python :: "

    return [classifier[len(prefix) :].strip() for classifier in classifiers if classifier.startswith(prefix)]
