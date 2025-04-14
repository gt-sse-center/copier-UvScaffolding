# noqa: D100
from jinja2 import Environment
from jinja2.ext import Extension


# ----------------------------------------------------------------------
class ToPythonListExtension(Extension):
    """Extension to convert a string to a python list."""

    def __init__(self, environment: Environment) -> None:  # noqa: D107
        super().__init__(environment)

        # ----------------------------------------------------------------------
        def ToPythonList(value: str) -> list[str]:
            # Maintain a list of tuples that can be used to sort the python versions
            # by major and minor version numbers. The first element is the major/minor
            # tuple and the second is the string itself.
            versions: list[tuple[tuple[int, int], str]] = []

            for version in value.split(","):
                version = version.strip()  # noqa: PLW2901
                assert version

                major, minor = version.split(".")

                versions.append(((int(major), int(minor)), version))

            # Sort by the major/minor tuple
            versions.sort(key=lambda x: x[0])

            # Return the strings now that the elements have been sorted
            return [version[1] for version in reversed(versions)]

        # ----------------------------------------------------------------------

        environment.filters["to_python_list"] = ToPythonList
