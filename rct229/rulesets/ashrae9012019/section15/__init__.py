# Add all available rule modules in __all__
import importlib

__all__ = [
    "prm9012019rule13w27",
    "prm9012019rule53e59",
    "prm9012019rule70w33",
    "prm9012019rule80l56",
    "prm9012019rule87p01",
    "prm9012019rule88q15",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
