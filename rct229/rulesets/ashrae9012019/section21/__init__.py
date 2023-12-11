# Add all available rule modules in __all__
import importlib

__all__ = [
    "section21rule1",
    "section21rule2",
    "section21rule3",
    "section21rule4",
    "section21rule5",
    "section21rule6",
    "section21rule7",
    "section21rule8",
    "section21rule9",
    "section21rule10",
    "section21rule11",
    "section21rule12",
    "section21rule13",
    "section21rule14",
    "section21rule15",
    "section21rule16",
    "section21rule17",
    "section21rule18",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
