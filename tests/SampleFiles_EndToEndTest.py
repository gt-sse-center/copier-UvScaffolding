import pytest

from dbrownell_Common import SubprocessEx

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_RuffFormat(copie) -> None:
    """Ensure that the ruff format command works on generated files."""

    output_dir = TestHelpers.RunTest(
        copie,
        next(TestHelpers.ConfigurationInfo.Generate()).configuration,
    )
    assert output_dir is not None

    result = SubprocessEx.Run("uv run ruff format --check", output_dir)
    assert result.returncode == 0, result.output
    assert "files already formatted" in result.output


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_RuffCheck(copie) -> None:
    """Ensure that the ruff check command works on generated files."""

    output_dir = TestHelpers.RunTest(
        copie,
        next(TestHelpers.ConfigurationInfo.Generate()).configuration,
    )
    assert output_dir is not None

    # The generated `__init__.py` file will have some known issues as uv adds some content when
    # it is generated and we append some content to it. Disable those checks when ensuring that
    # linting works as expected.
    result = SubprocessEx.Run(
        'uv run ruff check --per-file-ignores "__init__.py:D103,__init__.py:D104,__init__.py:RUF100"',
        output_dir,
    )
    assert result.returncode == 0, result.output
    assert "All checks passed!" in result.output
