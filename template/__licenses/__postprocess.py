import shutil

from pathlib import Path


# ----------------------------------------------------------------------
def Execute() -> None:
    dest_file = Path.cwd() / "LICENSE"
    if dest_file.is_file():
        dest_file.unlink()

    if "{{ license }}" != "None":  # noqa: PLR0133
        licenses_dir = Path.cwd() / "__licenses"
        assert licenses_dir.is_dir(), licenses_dir

        source_file = licenses_dir / "{{ license }}_LICENSE.txt"
        assert source_file.is_file(), source_file

        shutil.move(source_file, dest_file)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
Execute()
