# Add all available rule modules in __all__
import importlib

__all__ = [
    "section15rule1",
    "section15rule2",
    "section15rule3",
    "section15rule4",
    "section15rule5",
    "section15rule6",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
