# Add all available rule modules in __all__
import importlib

__all__ = ["section21rule3", "section21rule4"]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
