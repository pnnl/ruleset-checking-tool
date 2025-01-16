# Add all available rule modules in __all__
import importlib

# TODO: Fix section5rule2 and section5rule49 - they currently cause exceptions
__all__ = [
    "prm9012019rule02s62",
    "prm9012019rule04o58",
    "prm9012019rule11q41",
    "prm9012019rule18s99",
    "prm9012019rule20r05",
    "prm9012019rule23m90",
    "prm9012019rule29j06",
    "prm9012019rule33l08",
    "prm9012019rule34b75",
    "prm9012019rule38m70",
    "prm9012019rule39f24",
    "prm9012019rule39k65",
    "prm9012019rule40d86",
    "prm9012019rule40i28",
    "prm9012019rule42c42",
    "prm9012019rule43n21",
    "prm9012019rule44m70",
    "prm9012019rule45p36",
    "prm9012019rule46p73",
    "prm9012019rule48v87",
    "prm9012019rule48w84",
    "prm9012019rule50m61",
    "prm9012019rule50p59",
    "prm9012019rule57c26",
    "prm9012019rule67a77",
    "prm9012019rule67j71",
    "prm9012019rule69u47",
    "prm9012019rule69v04",
    "prm9012019rule70u00",
    "prm9012019rule72a03",
    "prm9012019rule73o42",
    "prm9012019rule73r04",
    "prm9012019rule77j30",
    "prm9012019rule78j13",
    "prm9012019rule78r30",
    "prm9012019rule80o45",
    "prm9012019rule82y74",
    "prm9012019rule84u02",
    "prm9012019rule87g56",
    "prm9012019rule96n40",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
