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
    "section22rule8",
    "section22rule9",
    "section22rule10",
    "section22rule11",
    "section22rule12",
    "section22rule13",
    "section22rule14",
    "section22rule15",
    "section22rule16",
    "section22rule17",
    "section22rule18",
    "section22rule19",
    "section22rule20",
    "section22rule21",
    "section22rule22",
    "section22rule23",
    "section22rule24",
    "section22rule25",
    "section22rule26",
    "section22rule27",
    "section22rule28",
    "section22rule29",
    "section22rule30",
    "section22rule31",
    "section22rule32",
    "section22rule33",
    "section22rule34",
    "section22rule35",
    "section22rule36",
    "section22rule37",
    "section22rule38",
    "section22rule39",
    "section22rule40",
    "section22rule41",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
