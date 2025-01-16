# Add all available rule modules in __all__
import importlib

__all__ = [
    'prm9012019rule06a67',
    'prm9012019rule22a24',
    'prm9012019rule29g28',
    'prm9012019rule31d63',
    'prm9012019rule34f57',
    'prm9012019rule34r52',
    'prm9012019rule35d81',
    'prm9012019rule39a29',
    'prm9012019rule43l11',
    'prm9012019rule47b05',
    'prm9012019rule58s22',
    'prm9012019rule59p62',
    'prm9012019rule62u16',
    'prm9012019rule63n48',
    'prm9012019rule82a90',
    'prm9012019rule83m55',
    'prm9012019rule86n98',
    'prm9012019rule92f56'
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
