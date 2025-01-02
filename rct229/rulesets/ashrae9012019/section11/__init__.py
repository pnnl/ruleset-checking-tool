# Add all available rule modules in __all__
import importlib

__all__ = [
    "section11rule1",
    # "section11rule2",
    # "section11rule3",
    # "section11rule4",
    # "section11rule5",
    "section11rule6",
    "section11rule7",
    "section11rule8",
    "section11rule9",
    "section11rule10",
    "section11rule11",
    "section11rule12",
    "section11rule13",
    "section11rule14",
    "section11rule15",
    "section11rule16",
    "section11rule17",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
