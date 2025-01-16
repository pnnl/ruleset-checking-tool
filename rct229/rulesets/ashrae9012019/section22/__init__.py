# Add all available rule modules in __all__
import importlib

__all__ = [
    "prm9012019rule01b91",
    "prm9012019rule03q09",
    "prm9012019rule04g06",
    "prm9012019rule13x50",
    "prm9012019rule18j38",
    "prm9012019rule20a97",
    "prm9012019rule30m88",
    "prm9012019rule33w37",
    "prm9012019rule36t85",
    "prm9012019rule37a05",
    "prm9012019rule38d92",
    "prm9012019rule38u90",
    "prm9012019rule41d32",
    "prm9012019rule41z21",
    "prm9012019rule47d94",
    "prm9012019rule48h16",
    "prm9012019rule48s83",
    "prm9012019rule52s13",
    "prm9012019rule52t53",
    "prm9012019rule55f82",
    "prm9012019rule57w94",
    "prm9012019rule58a51",
    "prm9012019rule59b18",
    "prm9012019rule60w01",
    "prm9012019rule67l25",
    "prm9012019rule68h16",
    "prm9012019rule68r93",
    "prm9012019rule71o81",
    "prm9012019rule78g49",
    "prm9012019rule79g01",
    "prm9012019rule79u84",
    "prm9012019rule81f32",
    "prm9012019rule81j88",
    "prm9012019rule84g72",
    "prm9012019rule86p62",
    "prm9012019rule88r57",
    "prm9012019rule92d16",
    "prm9012019rule92r39",
    "prm9012019rule95f90",
    "prm9012019rule96z66",
    "prm9012019rule99f07",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
