# Add all available rule modules in __all__
import importlib

__all__ = [
    "prm9012019rule02c29",
    "prm9012019rule08a45",
    "prm9012019rule16x33",
    "prm9012019rule22c86",
    "prm9012019rule22l93",
    "prm9012019rule37d98",
    "prm9012019rule66m62",
    "prm9012019rule73a47",
    "prm9012019rule99c05",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
