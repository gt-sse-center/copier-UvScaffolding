# Contributing to copier-UvScaffolding

Thanks for your interest in improving this template! This document covers setting up a development environment, running tests, validating template output, and exercising the GitHub Actions workflows locally before opening a pull request.

> **Note:** This file is for contributors working on **this template repository**. The `template/CONTRIBUTING.md` file is the contribution guide that ships into projects *generated* by the template — don't confuse the two.

## Prerequisites

| Tool | Why | Install |
| --- | --- | --- |
| [uv](https://docs.astral.sh/uv/) | Drives the project, manages the venv, and runs the Copier template. | https://docs.astral.sh/uv/getting-started/installation/ |
| [git](https://git-scm.com/) | Required by Copier and AutoGitSemVer. | https://git-scm.com/downloads |
| [pre-commit](https://pre-commit.com/) | Format/lint hooks on commit. Installed as a dev dependency — no separate install needed. | (via `uv sync`) |
| [act](https://github.com/nektos/act) *(optional)* | Run GitHub Actions workflows locally. | https://nektosact.com/installation/ |

The repo's `.python-version` pins the Python interpreter used for development; `uv sync` will fetch it automatically if it isn't already on your machine.

## One-time setup

```bash
git clone https://github.com/gt-csse/copier-UvScaffolding
cd copier-UvScaffolding

# Install all runtime + dev dependencies into .venv (uv reads pyproject.toml's
# [dependency-groups.dev] block — no separate "extras" flag is needed).
uv sync

# Install the pre-commit hooks so they run on every commit.
uv run pre-commit install
```

`uv sync` installs the `dev` dependency group by default. If you ever need a runtime-only install, use `uv sync --no-dev`.

## Day-to-day development

All commands below assume you're at the repo root.

### Running the template against a scratch directory

The template can't be invoked with `copier copy <url>` because it depends on local Jinja extensions and post-generation tasks. Use `run.py` instead:

```bash
uv run run.py Copy   /tmp/scratch-project          # initial generation
uv run run.py Recopy /tmp/scratch-project          # re-render with current answers
uv run run.py Update /tmp/scratch-project          # update an existing project to template HEAD
```

`run.py` pre-flights with `uv self update --dry-run` and refuses to run if uv is out of date. Pass `--skip-uv-version-check` to bypass.

### Materializing every test permutation at once

To eyeball the matrix of generated outputs without going through pytest:

```bash
uv run python tests/GenerateTemplates.py /tmp/template-permutations
```

This produces one subdirectory per configuration (license × coverage-badge × signing × ty), with `.git` and `.venv` stripped, so you can `diff -r` between permutations.

### Tests

The test suite is end-to-end: each test renders the template via `pytest-copie` and snapshots the result with `syrupy`.

```bash
uv run pytest                                              # full suite
uv run pytest tests/All_EndToEndTest.py                    # one file
uv run pytest tests/All_EndToEndTest.py -k MIT             # one configuration
uv run pytest --no-cov                                     # skip coverage (faster)
```

After intentional changes to template output, regenerate the snapshot and commit the diff alongside your change:

```bash
uv run pytest --snapshot-update
```

Inspect `tests/__snapshots__/All_EndToEndTest.ambr` to confirm the diff matches what you intended — an accidental snapshot update is the easiest way to silently break the template.

### Lint and format

```bash
uv run ruff format          # format
uv run ruff format --check  # check only (what CI runs)
uv run ruff check           # lint
```

`template/**` is excluded from both lint and format because it contains Jinja syntax that isn't valid Python until rendered. `tests/**` is excluded from lint. Don't lift those exclusions — see `pyproject.toml`.

### Pre-commit

```bash
uv run pre-commit run              # run on staged files
uv run pre-commit run --all-files  # run across the whole tree
```

The configured hooks are `uv sync --frozen`, `uv run ruff format --check`, and `uv run ruff check` — matching what CI runs.

## Locally testing the CI workflows

The CI workflow (`.github/workflows/CICD.yml` → `CICD_impl.yml`) does two things on each push/PR: a `validate` job (pre-commit + pytest across an OS × Python matrix), and a `release` job that only fires on `main`.

You have two options for local validation:

### Option A — Run the same commands CI runs (recommended)

The validate job's full command sequence is just:

```bash
uv sync
uv run pre-commit run --verbose
uv run pytest
```

If those three pass locally on a clean clone, the validate job will almost certainly pass too. This is faster, requires no extra tooling, and is what most contributors should do.

### Option B — Run the workflow via `act`

If you need to debug workflow YAML changes themselves (matrix expansion, conditionals, action versions), use [`act`](https://github.com/nektos/act):

```bash
# Run the full CI+CD workflow against the default event (push).
act push -W .github/workflows/CICD.yml

# Run only the pull_request trigger.
act pull_request -W .github/workflows/CICD.yml

# Restrict to a single job and a single Python version to keep the matrix small.
act push -W .github/workflows/CICD.yml -j validate \
  --matrix os:ubuntu-latest --matrix python_version:3.13
```

Notes when using `act`:

- The matrix in `CICD.yml` includes `macos-latest` and `windows-latest`; `act` only runs Linux containers, so trim the matrix with `--matrix` flags or by overriding the inputs.
- The `release` job is gated on `github.event_name == 'push' && github.ref == 'refs/heads/main'`, so it will be skipped locally unless you fake those values.
- Some actions (e.g., `astral-sh/setup-uv`) cache state under `~/.cache/act` — clear it if you see stale-cache surprises.

### Pull request checks

Before opening a PR, make sure all of these are green locally:

```bash
uv run pre-commit run --all-files
uv run pytest
```

If you updated snapshots, double-check the `.ambr` diff is intentional and minimal.

## Pull request workflow

1. Branch from `main` using a short, descriptive name (e.g., `61-add-contrib-docs`).
2. Keep changes focused — one logical change per PR.
3. Update or add tests. Template-output changes should land with a corresponding `--snapshot-update`.
4. Fill in the PR template (`.github/pull_request_template.md`) — especially the linked issue or work item.
5. Push and open the PR against `main`.

## Reporting bugs and requesting features

Use the issue templates at https://github.com/gt-csse/copier-UvScaffolding/issues. For security issues, follow `template/SECURITY.md` (which is the policy that ships with generated projects and mirrors this repo's own policy).
