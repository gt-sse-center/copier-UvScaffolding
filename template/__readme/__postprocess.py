from dataclasses import dataclass
from pathlib import Path


DELIMITER1 = "<!-- Content above this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->"
DELIMITER2 = "<!-- Content below this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->"


def Execute():
    # Load the information form the fragment
    fragment_filename = Path(__file__).parent / "__README.fragment.md"
    assert fragment_filename.is_file(), fragment_filename

    fragment_content = _Content.Load(fragment_filename, missing_delimiter_is_error=True)

    # Load the information form the README file
    readme_filename = Path(__file__).parent.parent / "README.md"
    readme_content = _Content.Load(readme_filename, missing_delimiter_is_error=False)

    with readme_filename.open("w", encoding="utf-8") as f:
        assert fragment_content.pre_content is not None
        f.write(fragment_content.pre_content)
        f.write("\n\n")

        assert fragment_content.default_content is not None
        f.write(readme_content.default_content or fragment_content.default_content)
        f.write("\n\n")

        assert fragment_content.post_content is not None
        f.write(fragment_content.post_content)
        f.write("\n")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class _Content:
    """Contains content read from a README.md file or fragment."""

    pre_content: str | None  # Content before the first delimiter
    default_content: str | None  # Content between the two delimiters
    post_content: str | None  # Content after the second delimiter

    @classmethod
    def Load(
        cls,
        filename: Path,
        *,
        missing_delimiter_is_error: bool=True,
    ) -> "_Content":
        if not filename.is_file():
            return cls(None, None, None)

        content = filename.read_text(encoding="utf-8")

        # Get the content indexes
        pre_content_index = content.find(DELIMITER1)
        post_content_index = content.find(DELIMITER2)

        if pre_content_index == -1 and missing_delimiter_is_error:
            raise ValueError(f"The delimiter '{DELIMITER1}' was not found in '{filename}'.")
        if post_content_index == -1 and missing_delimiter_is_error:
            raise ValueError(f"The delimiter '{DELIMITER2}' was not found in '{filename}'.")
        if pre_content_index != -1 and post_content_index != -1 and post_content_index < pre_content_index:
            raise ValueError(f"The delimiter '{DELIMITER2}' appears before '{DELIMITER1}' in '{filename}'.")

        if pre_content_index != -1:
            pre_content_index += len(DELIMITER1)

        # Get the content
        pre_content: str | None = None
        default_content: str | None = None
        post_content: str | None = None

        if pre_content_index != -1:
            pre_content = content[:pre_content_index].rstrip()

        if post_content_index != -1:
            post_content = content[post_content_index:].rstrip()

        if pre_content is None:
            if post_content is not None:
                default_content = content[:post_content_index].strip()
        elif post_content is None:
            if pre_content is not None:
                default_content = content[pre_content_index:].strip()
        else:
            default_content = content[pre_content_index:post_content_index].strip()

        # Create the object
        return cls(pre_content, default_content, post_content)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
Execute()
