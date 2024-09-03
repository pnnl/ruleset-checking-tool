# Add all available rule modules in __all__
import importlib

__all__ = [
    "section12rule1",
    "section12rule2",
    "section12rule3",
    "section12rule4",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
