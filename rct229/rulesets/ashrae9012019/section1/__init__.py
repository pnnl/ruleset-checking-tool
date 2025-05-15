import importlib

# Add all available rule modules in __all__
__all__ = [
    "section1rule1",
    "section1rule2",
    "section1rule3",
    "section1rule4",
    "section1rule5",
    "section1rule6",
    "section1rule7",
    "section1rule8",
    "section1rule9",
]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
