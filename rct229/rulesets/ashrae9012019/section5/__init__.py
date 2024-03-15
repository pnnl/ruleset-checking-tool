# Add all available rule modules in __all__
import importlib

# TODO: Fix section5rule2 and section5rule49 - they currently cause exceptions
__all__ = [
    "section5rule1",
    "section5rule2",
    "section5rule3",
    "section5rule4",
    "section5rule5",
    "section5rule6",
    "section5rule7",
    "section5rule8",
    "section5rule9",
    "section5rule10",
    "section5rule11",
    "section5rule12",
    "section5rule13",
    "section5rule14",
    "section5rule15",
    "section5rule16",
    "section5rule17",
    "section5rule18",
    "section5rule19",
    "section5rule20",
    "section5rule21",
    "section5rule22",
    "section5rule23",
    "section5rule24",
    "section5rule25",
    "section5rule26",
    "section5rule27",
    "section5rule28",
    "section5rule29",
    "section5rule30",
    "section5rule31",
    "section5rule32",
    "section5rule33",
    "section5rule34",
    "section5rule35",
    "section5rule36",
    "section5rule37",
    "section5rule38",
    "section5rule39",
    "section5rule40",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
