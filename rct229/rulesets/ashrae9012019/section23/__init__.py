# Add all available rule modules in __all__
import importlib

__all__ = [
    "prm9012019rule14m33",
    "prm9012019rule18u93",
    "prm9012019rule44u85",
    "prm9012019rule45r08",
    "prm9012019rule46w18",
    "prm9012019rule47f22",
    "prm9012019rule50v48",
    "prm9012019rule52x31",
    "prm9012019rule62j00",
    "prm9012019rule68z84",
    "prm9012019rule69z86",
    "prm9012019rule71f87",
    "prm9012019rule71k98",
    "prm9012019rule79i34",
    "prm9012019rule79m01",
    "prm9012019rule98g04",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
