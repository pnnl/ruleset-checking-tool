import importlib

# Add all available rule modules in __all__
__all__ = [
    "prm9012019rule03a79",
    "prm9012019rule30t80",
    "prm9012019rule34h06",
    "prm9012019rule55z67",
    "prm9012019rule66a48",
    "prm9012019rule92n36",
    "prm9012019rule98t42",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
