# noqa: D100
import shutil
import textwrap

from pathlib import Path

from rich import print


shutil.rmtree("__licenses")
shutil.rmtree("__post_generation_instructions")
shutil.rmtree("__readme")

Path("AutoGitSemVer.yaml").unlink()


content = textwrap.dedent(
    """\



    [green]Your project is almost complete![/]

    To finish generating your project, please follow the steps in [yellow]./post_generation_instructions.html[/][default].[/]


    """,
)

content = "\n".join(f"     {line}" for line in content.splitlines())

print(content)
print("\n")
