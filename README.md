# copier-UvScaffolding
Copier (https://copier.readthedocs.io/) template to create [uv](https://docs.astral.sh/uv/)-based python scaffolding.

**Functionality Includes:**

- Project/package scaffolding via [uv](https://docs.astral.sh/uv/)
- Open source license (`None`, `Apache-2.0`, `BSD-3-Clause-Clear`, `BSL-1.0`, `GPL-3.0-or-later`, `MIT`)
- Code formatting via [ruff](https://github.com/astral-sh/ruff)
- Static code analysis via [ruff](https://github.com/astral-sh/ruff)
- Pre commit-scripts via [pre-commit](https://pre-commit.com/)
- Automated test execution via [pytest](https://docs.pytest.org/)
- Code coverage extraction via [coverage](https://coverage.readthedocs.io/)
- Automatic [semantic version](https://semver.org/) generation via [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer)
- Python package creation via [uv](https://github.com/astral-sh/uv)
- Python package publishing to [PyPi](https://pypi.org/) via [uv](https://github.com/astral-sh/uv)
- Continuous [Integration](https://en.wikipedia.org/wiki/Continuous_integration) / [Delivery](https://en.wikipedia.org/wiki/Continuous_delivery) / [Deployment](https://en.wikipedia.org/wiki/Continuous_deployment) via [GitHub Actions](https://github.com/features/actions)
- GitHub [Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- GitHub [Pull Request Template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- Standard documentation (`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `DEVELOPMENT.md`, `GOVERNANCE.md`, `MAINTAINERS.md`, `README.md`, `SECURITY.md`)
- [Optional] Generation of code coverage badge displayed on `README.md`
- [Optional] Artifact signing via [py-minisign](https://github.com/x13a/py-minisign)

## How to use copier-UvScaffolding
This repository is a [copier](https://copier.readthedocs.io/) template. However, it is a template with advanced functionality that requires external python packages to function correctly. As a result, the template must be cloned and initialized before it can be used with `copier`.

### One-time Initialization

| Description | Command Line |
| --- | --- |
| 1) Install uv (if it isn't already installed). | https://docs.astral.sh/uv/getting-started/installation/ |
| 2) Clone this repository. | `git clone https://github.com/gt-sse-center/copier-UvScaffolding`
| 3) Initialize your local enlistment. | `uv sync` |

### Invoke `copier`
In each scenario, navigate to your local `copier-UvScaffolding` enlistment and run of of these commands, replacing `<output_dir>` with the path where content should be generated.

| Scenario | Description | Command Line |
| --- | --- | --- |
| Copy | Command used to initialize a repository. | `uv run copier copy . <output_dir> --trust` |
| Recopy | Command used to recopy template content. | `uv run copier recopy <output_dir> --trust` |
| Update | Command used to update a repository with old template content with new template content. | `uv run copier update <output_dir> --trust` |
