import importlib
import inspect

import rct229.rule_engine.rule_base as base_classes
import rct229.rules as rules

# Add all available rule modules in __all__
__all__ = ["section15"]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getrules__():
    modules = [f for f in inspect.getmembers(rules, inspect.ismodule)]
    base_class_names = [f[0] for f in inspect.getmembers(base_classes, inspect.isclass)]

    available_rules = []
    for module in modules:
        available_rules += [
            f
            for f in inspect.getmembers(module[1], inspect.isclass)
            if (not f[0].startswith("_")) and (not f[0] in base_class_names)
        ]
    return available_rules


def __dir__():
    return sorted(__all__)
