**Project:**
[![License](https://img.shields.io/github/license/{{ github_username }}/{{ github_repo_name }}?color=dark-green)]({{ github_url }}/blob/master/LICENSE)

**Package:**
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ python_package_name }}?color=dark-green)](https://pypi.org/project/{{ python_package_name }}/)
[![PyPI - Version](https://img.shields.io/pypi/v/{{ python_package_name }}?color=dark-green)](https://pypi.org/project/{{ python_package_name }}/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/{{ python_package_name }})](https://pypistats.org/packages/{{ python_package_name }})

**Development:**
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![CI]({{ github_url }}/actions/workflows/CICD.yml/badge.svg)]({{ github_url }}/actions/workflows/CICD.yml)
{%- if coverage_badge_gist_id != "" %}
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/{{ coverage_badge_gist_username }}/{{ coverage_badge_gist_id }}/raw/{{ github_repo_name }}_code_coverage.json)]({{ github_url }}/actions)
{%- endif %}
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/{{ github_username }}/{{ github_repo_name }}?color=dark-green)]({{ github_url }}/commits/main/)

<!-- Content above this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->

## Contents
- [Overview](#overview)
- [Installation](#installation)
- [Development](#development)
- [Additional Information](#additional-information)
{%- if license != "None" %}
- [License](#license)
{%- endif %}

## Overview
TODO: Complete this section

### How to use {{ project_name }}
TODO: Complete this section

<!-- Content below this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->

## Installation

| Installation Method | Command |
| --- | --- |
| Via [uv](https://github.com/astral-sh/uv) | `uv add {{ python_package_name }}` |
| Via [pip](https://pip.pypa.io/en/stable/) | `pip install {{ python_package_name }}` |

## Development
Please visit [Contributing]({{ github_url }}/blob/main/CONTRIBUTING.md) and [Development]({{ github_url }}/blob/main/DEVELOPMENT.md) for information on contributing to this project.

## Additional Information
Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
| Code of Conduct | [CODE_OF_CONDUCT.md]({{ github_url }}/blob/main/CODE_OF_CONDUCT.md) | Information about the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | [CONTRIBUTING.md]({{ github_url }}/blob/main/CONTRIBUTING.md) | Information about contributing to this project. |
| Development | [DEVELOPMENT.md]({{ github_url }}/blob/main/DEVELOPMENT.md) | Information about development activities involved in making changes to this project. |
| Governance | [GOVERNANCE.md]({{ github_url }}/blob/main/GOVERNANCE.md) | Information about how this project is governed. |
| Maintainers | [MAINTAINERS.md]({{ github_url }}/blob/main/MAINTAINERS.md) | Information about individuals who maintain this project. |
| Security | [SECURITY.md]({{ github_url }}/blob/main/SECURITY.md) | Information about how to privately report security issues associated with this project. |

{% if license != "None" -%}
## License
{{ project_name }} is licensed under the <a href="https://choosealicense.com/licenses/{{ license }}/" target="_blank">{{ license }}</a> license.
{%- endif %}
