__all__ = ("include_def", "include_variable")


def include_def():
    print(__name__)


def exclude_def():
    print(__name__)


_under_score = "under_score"
include_variable = "include_variable"
exclude_variable = "exclude_variable"
