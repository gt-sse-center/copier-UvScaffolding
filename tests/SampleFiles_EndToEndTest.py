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
@pytest.fixture
def extra_ruff_check_args() -> str:
    return '--per-file-ignores "__init__.py:D103,__init__.py:D104,__init__.py:RUF100"'


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_RuffFormat(generated_template_dir) -> None:
    """Ensure that the ruff format command works on generated files."""

    result = SubprocessEx.Run("uv run ruff format --check", generated_template_dir)
    assert result.returncode == 0, result.output
    assert "files already formatted" in result.output


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_RuffCheck(generated_template_dir, extra_ruff_check_args) -> None:
    """Ensure that the ruff check command works on generated files."""

    # The generated `__init__.py` file will have some known issues as uv adds some content when
    # it is generated and we append some content to it. Disable those checks when ensuring that
    # linting works as expected.
    result = SubprocessEx.Run(
        f"uv run ruff check {extra_ruff_check_args}",
        generated_template_dir,
    )
    assert result.returncode == 0, result.output
    assert "All checks passed!" in result.output


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_Pytest(generated_template_dir) -> None:
    """Ensure that pytest works on generated files."""

    # Note that uv introduces a function in __init__.py that is not exercised in the tests. Code
    # coverage fails because the code isn't covered. So, when we run here, run without coverage.
    result = SubprocessEx.Run("uv run pytest --no-cov", generated_template_dir)
    assert result.returncode == 0, result.output


# ----------------------------------------------------------------------
@pytest.mark.filterwarnings("ignore:Dirty template changes included automatically")
def test_PreCommit(generated_template_dir, extra_ruff_check_args) -> None:
    """Ensure that pre-commit works on generated files."""

    # Update the precommit script to augment the call to ruff check, similar to what we do in
    # test_RuffCheck.
    pre_commit_file = generated_template_dir / ".pre-commit-config.yaml"
    assert pre_commit_file.is_file(), pre_commit_file

    content = pre_commit_file.read_text(encoding="utf-8")
    content = content.replace("uv run ruff check", f"uv run ruff check {extra_ruff_check_args}")

    pre_commit_file.write_text(content, encoding="utf-8")

    # Run the script
    result = SubprocessEx.Run("uv run pre-commit run", generated_template_dir)
    assert result.returncode == 0, result.output
