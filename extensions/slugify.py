# noqa: D100
import re
import unicodedata

from typing import Protocol

from jinja2 import Environment
from jinja2.ext import Extension


class IfyFuncType(Protocol):  # noqa: D101
    def __call__(self, value: str, *, allow_unicode: bool = False) -> str: ...  # noqa: D102


# taken from Django
# https://github.com/django/django/blob/main/django/utils/text.py
def create_ify_func(
    separator: str,
) -> IfyFuncType:
    """Create a slugify function with different separators."""

    # ----------------------------------------------------------------------
    def ify(value: str, *, allow_unicode: bool = False) -> str:
        """\
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """

        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize("NFKC", value)
        else:
            value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        value = re.sub(r"[^\w\s-]", "", value)
        return re.sub(r"[-\s]+", separator, value)

    # ----------------------------------------------------------------------

    return ify


class SlugifyExtension(Extension):
    """Extension to convert a string to a slug."""

    def __init__(self, environment: Environment) -> None:  # noqa: D107
        super().__init__(environment)
        environment.filters["slugify"] = create_ify_func("-")


class PythonPackageifyExtension(Extension):
    """Extension to convert a string to a python package name."""

    def __init__(self, environment: Environment) -> None:  # noqa: D107
        super().__init__(environment)

        func = create_ify_func("_")

        environment.filters["pythonpackageify"] = lambda *args, **kwargs: func(*args, **kwargs).lower()


class PythonStrictPackageifyExtension(Extension):
    """Extension to convert a string to a strict python package name (all lowercase, underscores are converted to dashes)."""

    def __init__(self, environment: Environment) -> None:  # noqa: D107
        super().__init__(environment)

        func = create_ify_func("_")

        environment.filters["strictpythonpackageify"] = (
            lambda *args, **kwargs: func(*args, **kwargs).lower().replace("_", "-")
        )
