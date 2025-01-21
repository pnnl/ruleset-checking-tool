# Add all available rule modules in __all__
import importlib

__all__ = [
    "prm9012019rule06k20",
    # "section11rule2",
    # "section11rule3",
    # "section11rule4",
    # "section11rule5",
    "prm9012019rule23k17",
    "prm9012019rule29i55",
    "prm9012019rule29n09",
    "prm9012019rule40i48",
    "prm9012019rule49y39",
    "prm9012019rule51s51",
    "prm9012019rule52y79",
    "prm9012019rule62z26",
    "prm9012019rule63z32",
    "prm9012019rule72v93",
    "prm9012019rule76q85",
    "prm9012019rule93n40",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
