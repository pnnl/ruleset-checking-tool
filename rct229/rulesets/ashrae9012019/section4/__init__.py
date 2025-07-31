# Add all available rule modules in __all__
import importlib

__all__ = [
    "section4rule1",
    "section4rule2",
    "section4rule11",
    "section4rule14",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
