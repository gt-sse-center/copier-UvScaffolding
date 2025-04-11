# noqa: D100
import sys

from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common.Streams.StreamDecorator import StreamDecorator
from dbrownell_Common import SubprocessEx
import tomlkit


# ----------------------------------------------------------------------
def Execute() -> None:  # noqa: D103
    indented_stream = StreamDecorator(sys.stdout, "     ")

    if not _RunUvInit(indented_stream):
        return

    if not _AugmentGitignore(indented_stream):
        return

    if not _AugmentPyProject(indented_stream):
        return

    if not _AugmentInitFile(indented_stream):
        return

    indented_stream.write("\n")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _RunUvInit(indented_stream: StreamDecorator) -> bool:
    with DoneManager.Create(
        indented_stream,
        "Running uv init...",
        suffix="\n",
    ) as dm:
        if (Path.cwd() / "pyproject.toml").exists():
            dm.WriteLine("'pyproject.toml' already exists.")
        else:
            # Run uv init
            command_line = 'uv init --name "{{ python_package_name }}" --package --lib'

            dm.WriteVerbose(f"Command line: {command_line}\n\n")

            result = SubprocessEx.Run(command_line)

            dm.result = result.returncode
            if dm.result != 0:
                dm.WriteError(result.output)
                return False

            # Add dev dependencies
            dev_dependencies = [
                "autogitsemver",
                "pre-commit",
                "pytest",
                "pytest-cov",
                "ruff",
            ]

            command_line = f"uv add {' '.join(dev_dependencies)} --dev"

            dm.WriteVerbose(f"Command line: {command_line}\n\n")

            result = SubprocessEx.Run(command_line)

            dm.result = result.returncode
            if dm.result != 0:
                dm.WriteError(result.output)
                return False

    return True


# ----------------------------------------------------------------------
def _AugmentGitignore(indented_stream: StreamDecorator) -> bool:
    # ----------------------------------------------------------------------
    def Impl(
        source: str,
        fragment: str,
    ) -> str | None:
        updated_source = False

        source = source.rstrip()

        for line in fragment.splitlines():
            if line.startswith("#"):
                continue

            if line in source:
                continue

            updated_source = True
            source += "\n" + line

        return source if updated_source else None

    # ----------------------------------------------------------------------

    # Sometimes, for reasons that I don't understand, the .gitignore file is not created. Create an
    # empty one if it doesn't exist.
    gitignore_file = Path.cwd() / ".gitignore"
    if not gitignore_file.is_file():
        gitignore_file.touch()

    _AugmentHelper(
        indented_stream,
        "Augmenting '.gitignore'...",
        Path.cwd() / ".gitignore",
        Path.cwd() / "__.gitignore.fragment",
        Impl,
    )

    return True


# ----------------------------------------------------------------------
def _AugmentPyProject(indented_stream: StreamDecorator) -> bool:
    # ----------------------------------------------------------------------
    def _MergeDictionaries(
        source: dict[str, Any],
        dest: dict[str, Any],
    ) -> None:
        for source_key, source_value in source.items():
            if source_key not in dest:
                dest[source_key] = source_value
                continue

            dest_value = dest[source_key]
            if isinstance(source_value, dict) and isinstance(dest_value, dict):
                _MergeDictionaries(source_value, dest_value)
                continue

            # If here, the value already exists in the dest; keep that original value

    # ----------------------------------------------------------------------

    with DoneManager.Create(
        indented_stream,
        "Augmenting 'pyproject.toml'...",
    ):
        pyproject_file = Path.cwd() / "pyproject.toml"
        assert pyproject_file.is_file(), pyproject_file

        fragment_file = Path.cwd() / "__pyproject.fragment.toml"
        assert fragment_file.is_file(), fragment_file

        with pyproject_file.open() as f:
            destination = tomlkit.load(f)

        with fragment_file.open() as f:
            source = tomlkit.load(f)

        _MergeDictionaries(source, destination)

        project_section = cast("tomlkit.TOMLDocument", destination["project"])

        # Remove the hard-coded version, as __pyproject.fragment.toml is making it dynamic
        project_section.pop("version", None)

        # Always overwrite the license value, as it may have changed
        if "{{ license }}" == "None":  # noqa: PLR0133
            project_section.pop("license", None)
        else:
            project_section["license"] = {"text": "{{ license }}"}

        # Write the updated content
        with pyproject_file.open("w") as f:
            tomlkit.dump(destination, f)

        fragment_file.unlink()

    return True


# ----------------------------------------------------------------------
def _AugmentInitFile(indented_stream: StreamDecorator) -> bool:
    # ----------------------------------------------------------------------
    def Impl(
        source: str,
        fragment: str,
    ) -> str | None:
        if "__version__" in source:
            return None

        return source.rstrip() + "\n\n\n" + fragment

    # ----------------------------------------------------------------------

    _AugmentHelper(
        indented_stream,
        "Augmenting 'src/{{ python_package_name }}/__init__.py'...",
        Path.cwd() / "src" / "{{ python_package_name }}" / "__init__.py",
        Path.cwd() / "src" / "{{ python_package_name }}" / "____init__.fragment.py",
        Impl,
    )

    return True


# ----------------------------------------------------------------------
def _AugmentHelper(
    indented_stream: StreamDecorator,
    description: str,
    source_filename: Path,
    fragment_filename: Path,
    decorate_callback: Callable[[str, str], str | None],
) -> None:
    assert source_filename.is_file(), source_filename
    assert fragment_filename.is_file(), fragment_filename

    with DoneManager.Create(indented_stream, description):
        source_content = source_filename.read_text(encoding="utf-8")
        fragment_content = fragment_filename.read_text(encoding="utf-8")

        decorated_content = decorate_callback(source_content, fragment_content)
        if decorated_content is not None:
            source_filename.write_text(decorated_content, encoding="utf-8")

        fragment_filename.unlink()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
Execute()
