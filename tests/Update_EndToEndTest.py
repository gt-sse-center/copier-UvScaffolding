from io import StringIO

import pytest

from dbrownell_Common import SubprocessEx

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_Update(copie) -> None:
    """Ensure that update scenarios don't update unexpected files."""

    configuration = next(TestHelpers.ConfigurationInfo.Generate()).configuration
    configuration["_sign_artifacts_simulate_keygen"] = False

    # Note that an update bug was addressed in v0.2.2. Any version after that should be acceptable
    # here, as long as new, non-default variables have not been added to the template.
    output_dir = TestHelpers.RunTest(copie, configuration, ref="v0.2.2")
    assert output_dir is not None

    public_key_filename = output_dir / "minisign_key.pub"
    assert public_key_filename.is_file(), public_key_filename

    # Commit the changes (update can't operate on an uncommitted directory)
    for command_line in [
        'git config user.name "First last"',
        'git config user.email "a@b.com"',
        "git add --all",
        'git commit --message "Initial commit"',
    ]:
        command_sink = StringIO()

        result = SubprocessEx.Stream(command_line, command_sink, cwd=output_dir)
        command_sink = command_sink.getvalue()

        assert result == 0, (result, command_sink)

    # Run the update
    command_line = f'copier update "{output_dir}" --trust --defaults --vcs-ref=HEAD'
    update_sink = StringIO()

    result = SubprocessEx.Stream(command_line, update_sink)
    update_sink = update_sink.getvalue()

    assert result == 0, (result, update_sink)

    # Validate that the update did not change the public key
    assert public_key_filename.is_file(), public_key_filename

    command_line = f'git status --short "{public_key_filename.name}"'
    status_sink = StringIO()

    result = SubprocessEx.Stream(command_line, status_sink)
    status_sink = status_sink.getvalue()

    assert result == 0, (result, status_sink)
    assert not status_sink, status_sink
