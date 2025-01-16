import importlib

# Add all available rule modules in __all__
__all__ = [
    'prm9012019rule10d53',
    'prm9012019rule37e66',
    'prm9012019rule60m79',
    'prm9012019rule63e94',
    'prm9012019rule73j65',
    'prm9012019rule86h31',
    'prm9012019rule88z11',
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
