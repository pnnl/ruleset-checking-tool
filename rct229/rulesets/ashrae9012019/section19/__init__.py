# Add all available rule modules in __all__
import importlib

__all__ = [
    "section19rule1",
    "section19rule2",
    "section19rule3",
    "section19rule4",
    "section19rule5",
    "section19rule6",
    "section19rule7",
    "section19rule8",
    "section19rule9",
    "section19rule10",
    "section19rule11",
    "section19rule12",
    "section19rule13",
    "section19rule14",
    "section19rule15",
    "section19rule16",
    "section19rule17",
    "section19rule18",
    "section19rule19",
    "section19rule20",
    "section19rule21",
    "section19rule22",
    "section19rule23",
    "section19rule24",
    "section19rule25",
    "section19rule26",
    "section19rule27",
    "section19rule28",
    "section19rule29",
    "section19rule30",
    "section19rule31",
    "section19rule32",
    "section19rule33",
    "section19rule34",
    "section19rule35",
    "section19rule36",
    "section19rule37",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
