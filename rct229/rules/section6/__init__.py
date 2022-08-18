# Add all available rule modules in __all__
import importlib

__all__ = [
    "section6rule1",
    "section6rule2",
    "section6rule3",
    "section6rule4",
    "section6rule5",
    "section6rule6",
    "section6rule7",
    "section6rule8",
    "section6rule9",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
