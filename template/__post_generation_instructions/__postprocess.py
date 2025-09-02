import textwrap

from pathlib import Path


PLACEHOLDER = "<!-- REPLACE ME -->"


def Execute():
    instructions: dict[str, str] = {}

    _CreateUpdateInstructions(instructions)
    _CreateGitHubSettings(instructions)
    _CreateTemporaryPyPiToken(instructions)
    _CreateMinisignSecret(instructions)
    _CreateUvInstructions(instructions)
    _CreatePreCommitInstructions(instructions)
    _CreateCommitInstructions(instructions)

    _CreateFinalPyPiToken(instructions)
    _CreateFinalInstructions(instructions)

    instruction_content = "\n".join(
        textwrap.dedent(
            """\
            <details>
              <summary>
                <span role="term"><input type="checkbox" id="{title_id}">{index}) {title}</span>
              </summary>
            </details>
            <div role="definition" class="details-content">
              {steps_html}
            </div>
            """,
        ).format(
            index=index + 1,
            title_id=title.lower().replace(" ", "-"),
            title=title,
            steps_html=instruction,
        )
        for index, (title, instruction) in enumerate(instructions.items())
    )

    # Read the fragment content
    fragment_filename = Path(__file__).parent / "post_generation_instructions.fragment.html"
    assert fragment_filename.is_file(), fragment_filename

    fragment_content = fragment_filename.read_text(encoding="utf-8")

    # Replace the placeholder
    fragment_content = fragment_content.replace(PLACEHOLDER, instruction_content)

    # Write the content
    post_generation_filename = Path(__file__).parent.parent / "post_generation_instructions.html"
    post_generation_filename.write_text(fragment_content, encoding="utf-8")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _CreateUpdateInstructions(instructions: dict[str, str]) -> None:
    instructions["Update MAINTAINERS.md"] = textwrap.dedent(
        """\
        <p>In this step, we will replace placeholder information in <code>MAINTAINERS.md</code> with information specific to your repository.</p>
        <ol>
          <li>Open <code>MAINTAINERS.md</code> in a text editor.</li>
          <li>Replace the placeholder maintainers in the table with your own information.</li>
        </ol>
        """,
    )

    instructions["Update pyproject.toml"] = textwrap.dedent(
        """\
        <p>In this step, we will replace information in <code>pyproject.toml</code> with information specific to your repository.</p>
        <ol>
          <li>Open <code>pyproject.toml</code> in a text editor.</li>
          <li>Scan the generated content and update it as necessary.</li>
        </ol>
        """,
    )


# ----------------------------------------------------------------------
def _CreateGitHubSettings(instructions: dict[str, str]) -> None:
    instructions["Update GitHub Settings"] = textwrap.dedent(
        """\
        <p>In this step, we will update GitHub settings to allow the creation of git tags during a release.</p>
        <ol>
          <li>Visit <a href="{{ github_url }}/settings/actions" target="_blank">{{ github_url }}/settings/actions</a>.</li>
          <li>In the "Workflow permissions" section...</li>
          <li>Select "Read and write permissions".</li>
          <li>Click the "Save" button.</li>
        </ol>
        """,
    )



# ----------------------------------------------------------------------
def _CreateTemporaryPyPiToken(instructions: dict[str, str]) -> None:
    # Create and save the temporary PyPi token
    instructions["Create a Temporary PyPi Token"] = textwrap.dedent(
        """\
        <p>In this step, we will create a temporary <a href="https://pypi.org" target="_blank">PyPi</a> token used to publish the python package for the first time. The token created will be scoped to all of your projects on PyPi (which provides too much access). Once the package has been published for the first time, we will delete this temporary token and create a new one that is scoped to the single project.</p>
        <ol>
          <li>Visit <a href="https://pypi.org/manage/account/token/" target="_blank">https://pypi.org/manage/account/token/</a>.</li>
          <li>
            <p>Enter the values:</p>
            <p>
              <table>
                <tr>
                  <th>Token name:</th>
                  <td><code>Temporary CI Publish Action ({{ python_package_name }})</code></td>
                </tr>
                <tr>
                  <th>Scope:</th>
                  <td><code>Entire account (all projects)</code></td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Create token" button.</li>
          <li>Click the "Copy token" button for use in the next step.</li>
        </ol>
        """,
    )

    instructions["Save the Temporary PyPi Token as a GitHub Secret"] = textwrap.dedent(
        """\
        <p>In this step, we will save the <a href="https://pypi.org" target="_blank">PyPi</a> token just created as a <a href="https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions" target="_blank">GitHub Action secret</a>.</p>
        <ol>
          <li>Visit <a href="{{ github_url }}/settings/secrets/actions/new" target="_blank">{{ github_url }}/settings/secrets/actions/new</a>.</li>
          <li>
            <p>Enter the values:</p>
            <p>
              <table>
                <tr>
                  <th>Name:</th>
                  <td><code>PYPI_PUBLISH_TOKEN</code></td>
                </tr>
                <tr>
                  <th>Secret:</th>
                  <td>&lt;paste the token generated in the previous step&gt;</td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Add secret" button.</li>
        </ol>
        """,
    )

{% if coverage_badge_gist_id %}
    instructions["Create a GitHub Personal Access Token for gists"] = textwrap.dedent(
        """\
        <p>In this step, we will create a GitHub Personal Access Token (PAT) used when persisting code coverage information between Continuous Integration runs.</p>
        <ol>
          <li>Visit <a href="{{ github_host }}/settings/tokens?type=beta" target="_blank">{{ github_host }}/settings/tokens?type=beta</a>.</li>
          <li>Click the "Generate new token" button.</li>
          <li>Name the token <code>GitHub Workflow Gist ({{ github_repo_name }})</code>.</li>
          <li>In the Repository access section...</li>
          <li>Select "Only select repositories"...</li>
          <li>Select <code>{{ github_repo_name }}</code>.</li>
          <li>In the "Permissions" section...</li>
          <li>Click on the "Account" tab...</li>
          <li>Click on the "Add permissions" button...</li>
          <li>Select the "Gists" checkbox.</li>
          <li>In the "Gists" list item that appears in the list of permissions...</li>
          <li>Ensure that "Access" is set to "Read and write".</li>
          <li>Click the "Generate token" button.</li>
          <li>Copy the token for use in the next step.</li>
        </ol>
        """,
    )

    instructions["Save the GitHub Personal Access Token for gists"] = textwrap.dedent(
        """\
        <p>In this step, we will save the GitHub Personal Access Token just created as a <a href="https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions" target="_blank">GitHub Action secret</a>.</p>
        <ol>
          <li>Visit <a href="{{ github_url }}/settings/secrets/actions/new" target="_blank">{{ github_url }}/settings/secrets/actions/new</a>.</li>
          <li>
            <p>Enter the values:</p>
            <p>
              <table>
                <tr>
                  <th>Name:</th>
                  <td><code>COVERAGE_BADGE_GIST_TOKEN</code></td>
                </tr>
                <tr>
                  <th>Secret:</th>
                  <td>&lt;paste the token generated in the previous step&gt;</td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Add secret" button.</li>
        </ol>
        """,
    )
{% endif %}


# ----------------------------------------------------------------------
def _CreateMinisignSecret(instructions: dict[str, str]) -> None:
{% if sign_artifacts_question %}
    instructions["Save the Minisign Private Key"] = textwrap.dedent(
        """\
        <p>In this step, we will save the <a href="https://github.com/x13a/py-minisign" target="_blank">Minisign</a> private key as a <a href="https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions" target="_blank">GitHub Action secret</a>.</p>
        <ol>
          <li>Open <code>minisign_key.pri</code> in a text editor and copy all of the contents.</li>
          <li>Visit <a href="{{ github_url }}/settings/secrets/actions/new" target="_blank">{{ github_url }}/settings/secrets/actions/new</a>.</li>
          <li>
            <p>Enter the values:</p>
            <p>
              <table>
                <tr>
                  <th>Name:</th>
                  <td><code>MINISIGN_PRIVATE_KEY</code></td>
                </tr>
                <tr>
                  <th>Secret:</th>
                  <td>&lt;paste the private key previously copied&gt;</td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Add secret" button.</li>
        </ol>
        """,
    )

    instructions["Store the Minisign Private Key"] = textwrap.dedent(
        """\
        <p>Store the <a href="https://github.com/x13a/py-minisign" target="_blank">Minisign</a> private key in a secure location. Once you have stored the key, you can delete it from your local machine.</p>
        <p>Note that you should NEVER force <code>minisign_key.pri</code> into source control.</p>
        """,
    )
{% else %}
    pass
{% endif %}


# ----------------------------------------------------------------------
def _CreateUvInstructions(instructions: dict[str, str]) -> None:
    instructions["Install uv locally"] = textwrap.dedent(
        """\
        <p>In this step, we will install <a href="https://docs.astral.sh/uv" target="_blank">uv</a> for local development (if necessary) and initialize its dependencies.</p>

        <p>To install <code>uv</code> locally, follow the instructions at <a href="https://docs.astral.sh/uv/#installation" target="_blank">https://docs.astral.sh/uv/#installation</a>.</p>

        <p>To initialize this repository's dependencies, open a terminal window, navigate to your repository, and run the following command:</p>

        1. <code>uv sync</code><br/>
        <p></p>
        """,
    )


# ----------------------------------------------------------------------
def _CreatePreCommitInstructions(instructions: dict[str, str]) -> None:
    instructions["Install pre-commit"] = textwrap.dedent(
        """\
        <p>In this step, we will initialize <a href="https://pre-commit.com/" target="_blank">pre-commit</a> so that checks are run as a part of every commit.</p>

        <p>Open a terminal window, navigate to your repository, and run the following command:</p>

        1. <code>uv run pre-commit install</code>
        <p></p>
        """,
    )


# ----------------------------------------------------------------------
def _CreateCommitInstructions(instructions: dict[str, str]) -> None:
    instructions["Initialize the git repository"] = textwrap.dedent(
        """\
        <p>In this step, we will commit the files generated in git and push the changes.</p>

        <p>Open a terminal window, navigate to your repository, and run the following commands:</p>

        1. <code>git add --all</code><br/>
        2. <code>git commit -m "🎉 Initial commit"</code><br/>
        3. <code>git push</code><br/>
        <p></p>
        """,
    )


# ----------------------------------------------------------------------
def _CreateFinalPyPiToken(instructions: dict[str, str]) -> None:
    instructions["Verify the CI/CD Workflow"] = textwrap.dedent(
        """\
        <p>In this step, we will verify that the GitHub Action workflow completed successfully.</p>
        <ol>
          <li>Visit <a href="{{ github_url }}/actions" target="_blank">{{ github_url }}/actions</a>.</li>
          <li>Select the most recent workflow.</li>
          <li>Wait for the workflow to complete successfully.</li>
        </ol>
        """,
    )

    instructions["Delete the temporary PyPi Token"] = textwrap.dedent(
        """\
        <p>In an earlier step, we created a temporary <a href="https://pypi.org" target="_blank">PyPi</a> token. In this step, we will delete that token. A new token to replace it will be created in the steps that follow.</p>
        <ol>
          <li>Visit <a href="https://pypi.org/manage/account/" target="_blank">https://pypi.org/manage/account/</a>.</li>
          <li>Find the token named <code>Temporary CI Publish Action ({{ python_package_name }})</code>...</li>
          <li>Click the "Options" dropdown button...</li>
          <li>Select "Remove token".</li>
          <li>In the dialog box that appears...</li>
          <li>Enter your password.</li>
          <li>Click the "Remove API token" button.</li>
        </ol>
        """,
    )

    instructions["Create an Official PyPi Token"] = textwrap.dedent(
        """\
        <p>In this step, we create a new token scoped only to "{{ python_package_name }}".</p>

        <ol>
          <li>Visit <a href="https://pypi.org/manage/account/token/" target="_blank">https://pypi.org/manage/account/token/</a>.</li>
          <li>
            <p>Enter the values:</p>
            <p>
              <table>
                <tr>
                  <th>Token name:</th>
                  <td><code>CI Publish Action ({{ python_package_name }})</code></td>
                </tr>
                <tr>
                  <th>Scope:</th>
                  <td><code>Project: {{ python_package_name }}</code></td>
                </tr>
              </table>
            </p>
          </li>
          <li>Click the "Create token" button.</li>
          <li>Click the "Copy token" button for use in the next step.</li>
        </ol>
        """,
    )

    instructions["Update the GitHub Secret with the Official PyPi Token"] = textwrap.dedent(
        """\
        <p>In this step, we will save the PyPi token just created as a <a href="https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions" target="_blank">GitHub Action secret</a>.</p>
        <ol>
          <li>Visit <a href="{{ github_url }}/settings/secrets/actions/PYPI_PUBLISH_TOKEN" target="_blank">{{ github_url }}/settings/secrets/actions/PYPI_PUBLISH_TOKEN</a>.</li>
          <li>In the "Value" text window, paste the token generated in the previous step.</li>
          <li>Click "Update secret".</li>
        </ol>
        """,
    )


# ----------------------------------------------------------------------
def _CreateFinalInstructions(instructions: dict[str, str]) -> None:
    instructions["Delete this file"] = textwrap.dedent(
        """\
        <p>After you have completed all the steps, you can delete this file.</p>
        <p>Now your project is ready to go!</p>
        """,
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
Execute()
