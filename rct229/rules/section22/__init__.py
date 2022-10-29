# Add all available rule modules in __all__
import importlib

__all__ = [
    "section22rule1",
    "section22rule2",
    "section22rule3",
    "section22rule4",
    "section22rule5",
    "section22rule6",
    "section22rule14",
    "section22rule16",
    "section22rule19",
    "section22rule20",
    "section22rule27",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
