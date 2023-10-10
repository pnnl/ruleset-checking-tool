# Add all available rule modules in __all__
import importlib

# TODO: Fix section5rule2 and section5rule49 - they currently cause exceptions
__all__ = [
    # "section5rule2",
    "section5rule10",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
