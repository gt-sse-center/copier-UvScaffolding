import os
import sys

from plumbum import local


def pytest_configure(config):
    # Pin uv's Python to the test runner's Python so subprocess `uv init`
    # calls in the template-render path produce a `.python-version` that
    # matches `sys.version_info` (what All_EndToEndTest.py:69 asserts).
    # CI does this implicitly via `astral-sh/setup-uv`; setdefault preserves
    # an explicit override (e.g. `UV_PYTHON=3.11 uv run pytest`).
    #
    # We also have to update `plumbum.local.env`: copier executes `_tasks`
    # via `subprocess.run(..., env=local.env)`, and plumbum's LocalEnv
    # snapshots `os.environ` at instantiation (which happens when pytest-copie
    # imports plumbum, before this hook runs). Updating only `os.environ`
    # would leave the snapshot stale and the variable wouldn't reach the
    # `uv init` subprocess.
    uv_python = os.environ.setdefault(
        "UV_PYTHON",
        ".".join(str(i) for i in sys.version_info[:2]),
    )
    local.env["UV_PYTHON"] = uv_python
