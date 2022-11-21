# Add all available rule modules in __all__
import importlib

__all__ = [
    "section22rule1",
    "section22rule2",
    "section22rule3",
    "section22rule4",
    "section22rule5",
    "section22rule6",
    "section22rule7",
    "section22rule9",
    "section22rule11",
    "section22rule14",
    "section22rule16",
    "section22rule19",
    "section22rule20",
    "section22rule21",
    "section22rule22",
    "section22rule23",
    "section22rule24",
    "section22rule27",
    "section22rule29",
    "section22rule30",
    "section22rule31",
    "section22rule32",
    "section22rule33",
    "section22rule34",
    "section22rule40",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
