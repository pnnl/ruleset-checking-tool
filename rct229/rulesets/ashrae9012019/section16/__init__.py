import importlib

# Add all available rule modules in __all__
__all__ = [
    "section16rule1",
    "section16rule2",
    "section16rule3",
    "section16rule4",
    "section16rule5",
    "section16rule6",
    "section16rule7",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
