# noqa: D100
import shutil

from pathlib import Path


shutil.rmtree("__licenses")

Path("AutoGitSemVer.yaml").unlink()
