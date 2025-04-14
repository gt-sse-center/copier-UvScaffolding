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

    classifiers = _GetPythonVersionClassifiers(
        TestHelpers.LoadPyproject(output_dir)["project"]["classifiers"]
    )
    assert classifiers

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

    new_classifiers = _GetPythonVersionClassifiers(
        TestHelpers.LoadPyproject(output_dir)["project"]["classifiers"]
    )
    assert all(new_version in new_classifiers for new_version in new_versions), (
        new_classifiers,
        new_versions,
    )
    assert len(new_classifiers) == len(new_versions), (new_classifiers, new_versions)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _GetPythonVersionClassifiers(classifiers: list[str]) -> list[str]:
    """Extracts the Python version classifiers from the provided list of classifiers."""

    prefix = "Programming Language :: Python :: "

    return [classifier[len(prefix) :].strip() for classifier in classifiers if classifier.startswith(prefix)]
