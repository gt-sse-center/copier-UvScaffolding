from pathlib import Path

import pytest

from dbrownell_Common import SubprocessEx

pytest.register_assert_rewrite("TestHelpers")
import TestHelpers


# ----------------------------------------------------------------------
@pytest.fixture
def generated_template_dir(copie) -> Path:
    generated_dir = TestHelpers.RunTest(
        copie,
        next(TestHelpers.ConfigurationInfo.Generate()).configuration,
    )

    assert generated_dir is not None
    return generated_dir


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_RuffFormat(generated_template_dir) -> None:
    """Ensure that the ruff format command works on generated files."""

    result = SubprocessEx.Run("uv run ruff format --check", generated_template_dir)
    assert result.returncode == 0, result.output
    assert "files already formatted" in result.output


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_RuffCheck(generated_template_dir) -> None:
    """Ensure that the ruff check command works on generated files."""

    result = SubprocessEx.Run(
        "uv run ruff check",
        generated_template_dir,
    )
    assert result.returncode == 0, result.output
    assert "All checks passed!" in result.output


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_Pytest(generated_template_dir) -> None:
    """Ensure that pytest works on generated files."""

    result = SubprocessEx.Run("uv run pytest", generated_template_dir)
    assert result.returncode == 0, result.output


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_PreCommit(generated_template_dir) -> None:
    """Ensure that pre-commit works on generated files."""

    result = SubprocessEx.Run("uv run pre-commit run", generated_template_dir)
    assert result.returncode == 0, result.output
