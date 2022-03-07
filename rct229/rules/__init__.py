import importlib
import inspect

import rct229.rule_engine.rule_base as base_classes
import rct229.rules as rules

# Add all available rule modules in __all__
__all__ = [
    "section5",
    "section6",
    "section12",
    "section15",
]


def __getrules__():
    modules = []
    __getrules_module__helper(rules, modules)
    base_class_names = [f[0] for f in inspect.getmembers(base_classes, inspect.isclass)]

    available_rules = []
    for module in modules:
        available_rules += [
            f
            for f in inspect.getmembers(module[1], inspect.isclass)
            if (not f[0].startswith("_")) and (not f[0] in base_class_names)
        ]
    return available_rules


def __getrules_module__helper(rules, module_list):
    inspect_results = inspect.getmembers(rules, inspect.ismodule)
    for f in inspect_results:
        if len(inspect.getmembers(f[1], inspect.ismodule)) == 0:
            module_list.append(f)
        else:
            __getrules_module__helper(f[1], module_list)


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
