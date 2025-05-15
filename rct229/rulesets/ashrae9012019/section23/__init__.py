# Add all available rule modules in __all__
import importlib

__all__ = [
    "section23rule1",
    "section23rule2",
    "section23rule3",
    "section23rule4",
    "section23rule5",
    "section23rule6",
    "section23rule7",
    "section23rule8",
    "section23rule9",
    "section23rule10",
    "section23rule11",
    "section23rule12",
    "section23rule13",
    "section23rule14",
    "section23rule15",
    "section23rule16",
    "section23rule17",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
