from io import StringIO
from pathlib import Path

import pytest

from dbrownell_Common import SubprocessEx
from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.Streams.StreamDecorator import StreamDecorator

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_GitOriginInstructionsNotIncludedWhenOriginExists(tmp_path: Path) -> None:
    """Verifies that instructions to add a git origin are not included when the target directory already has an origin."""

    configuration = next(TestHelpers.ConfigurationInfo.Generate()).configuration

    # Initialize a git repository with an origin in the target directory
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    for command_line in [
        "git init",
        'git config user.name "Test User"',
        'git config user.email "test@example.com"',
        "git remote add origin https://github.com/example/repo.git",
    ]:
        command_sink = StringIO()
        result = SubprocessEx.Stream(command_line, command_sink, cwd=output_dir)
        assert result == 0, (command_line, result, command_sink.getvalue())

    # Run the template generation
    with DoneManager.Create(StreamDecorator(None), "") as dm:
        TestHelpers.RunManually(
            dm,
            Path.cwd(),
            output_dir,
            configuration,
        )

    # Verify the post_generation_instructions.html does NOT contain git origin instructions
    instructions_file = output_dir / "post_generation_instructions.html"
    assert instructions_file.is_file(), instructions_file

    content = instructions_file.read_text(encoding="utf-8")
    assert "git remote add origin" not in content, (
        "Instructions should not include 'git remote add origin' when origin already exists"
    )
