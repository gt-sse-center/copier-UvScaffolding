from pathlib import Path

import pytest

from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.Streams.StreamDecorator import StreamDecorator

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_PreserveGeneratedKeys(copie) -> None:
    """Tests that the generated keys are preserved when copier is run a second time on an output directory."""

    configuration = next(TestHelpers.ConfigurationInfo.Generate()).configuration
    configuration["_sign_artifacts_simulate_keygen"] = False

    # Generate the default content
    output_dir = TestHelpers.RunTest(copie, configuration)
    assert output_dir is not None

    # Check that the keys were generated
    private_key_filename = output_dir / "minisign_key.pri"
    public_key_filename = output_dir / "minisign_key.pub"

    assert private_key_filename.is_file(), private_key_filename
    assert public_key_filename.is_file(), public_key_filename

    # Update the content
    with open(private_key_filename, encoding="utf-8") as f:
        original_private_key = f.read()

    with open(public_key_filename, encoding="utf-8") as f:
        original_public_key = f.read()

    # Generate again
    with DoneManager.Create(StreamDecorator(None), "") as dm:
        TestHelpers.RunManually(
            dm,
            Path.cwd(),
            output_dir,
            configuration,
        )

    new_private_key = private_key_filename.read_text(encoding="utf-8")
    new_public_key = public_key_filename.read_text(encoding="utf-8")

    assert new_private_key == original_private_key, (new_private_key, original_private_key)
    assert new_public_key == original_public_key, (new_public_key, original_public_key)

    # Delete the keys
    private_key_filename.unlink()
    public_key_filename.unlink()

    # Generate again
    with DoneManager.Create(StreamDecorator(None), "") as dm:
        TestHelpers.RunManually(
            dm,
            Path.cwd(),
            output_dir,
            configuration,
        )

    new_private_key = private_key_filename.read_text(encoding="utf-8")
    new_public_key = public_key_filename.read_text(encoding="utf-8")

    assert new_private_key != original_private_key, (new_private_key, original_private_key)
    assert new_public_key != original_public_key, (new_public_key, original_public_key)
