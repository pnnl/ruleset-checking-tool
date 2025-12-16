# Add all available rule modules in __all__
import importlib

__all__ = [
<<<<<<< RS/YJ/Rule_22-44-2022
    "section22rule44",
]

SHORT_NAME = "HVAC-CHW"

=======
    "section22rule42",
    "section22rule43",
]

>>>>>>> feature/ashrae-9012022

def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
