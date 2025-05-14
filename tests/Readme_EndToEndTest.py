from pathlib import Path

import pytest

from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.Streams.StreamDecorator import StreamDecorator

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_PreserveContentModifications(copie) -> None:
    """Tests that modifications to README.md are preserved when copier is run a second time on an output directory."""

    configuration = next(TestHelpers.ConfigurationInfo.Generate()).configuration

    # Generate the default content
    output_dir = TestHelpers.RunTest(copie, configuration)
    assert output_dir is not None

    readme_filename = output_dir / "README.md"
    assert readme_filename.is_file(), readme_filename

    readme_content = readme_filename.read_text(encoding="utf-8")

    assert "## Contents" in readme_content, readme_content
    assert "## Overview" in readme_content, readme_content
    assert "### How to use `this_is_the_project_name`" in readme_content, readme_content

    # Update the content
    assert "## Updated Contents" not in readme_content, readme_content
    readme_content = readme_content.replace("## Contents", "## Updated Contents")

    readme_filename.write_text(readme_content, encoding="utf-8")

    # Generate again
    with DoneManager.Create(StreamDecorator(None), "") as dm:
        TestHelpers.RunManually(
            dm,
            Path.cwd(),
            output_dir,
            configuration,
        )

    new_content = readme_filename.read_text(encoding="utf-8")

    assert "## Contents" not in new_content, new_content
    assert "## Updated Contents" in new_content, new_content
