# Add all available rule modules in __all__
import importlib

__all__ = [
    "prm9012019rule18y74",
    "prm9012019rule66c61",
    "prm9012019rule85i93",
    "prm9012019rule96q77",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
