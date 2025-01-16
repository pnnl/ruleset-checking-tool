# Add all available rule modules in __all__
import importlib

__all__ = [
    'prm9012019rule02h13',
    'prm9012019rule03j97',
    'prm9012019rule04f07',
    'prm9012019rule07w16',
    'prm9012019rule09g49',
    'prm9012019rule10q01',
    'prm9012019rule16j07',
    'prm9012019rule18u58',
    'prm9012019rule20g60',
    'prm9012019rule20z34',
    'prm9012019rule23q51',
    'prm9012019rule28i68',
    'prm9012019rule29n92',
    'prm9012019rule31y73',
    'prm9012019rule40n43',
    'prm9012019rule44t17',
    'prm9012019rule45j93',
    'prm9012019rule49c09',
    'prm9012019rule51d17',
    'prm9012019rule54e25',
    'prm9012019rule58x03',
    'prm9012019rule60d49',
    'prm9012019rule60f12',
    'prm9012019rule60o81',
    'prm9012019rule73r44',
    'prm9012019rule74p61',
    'prm9012019rule75k92',
    'prm9012019rule76q46',
    'prm9012019rule77j17',
    'prm9012019rule84b07',
    'prm9012019rule87f72',
    'prm9012019rule88f26',
    'prm9012019rule93f21',
    'prm9012019rule95r49',
    'prm9012019rule97a53',
    'prm9012019rule98o22'
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
