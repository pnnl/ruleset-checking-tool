import importlib
import inspect

import rct229.rule_engine.rule_base as base_classes
import rct229.rule_engine.rule_list_base as base_list_classes
import rct229.rule_engine.rule_list_indexed_base as base_list_indexed_classes
import rct229.rules as rules
from rct229.rule_engine.rule_base import RuleDefinitionBase

# Add all available rule modules in __all__
__all__ = ["section5", "section6", "section12", "section15", "section21", "section22"]


def __getrules__():
    modules = []
    __getrules_module__helper(rules, modules)
    base_class_names = [f[0] for f in inspect.getmembers(base_classes, inspect.isclass)]
    base_class_names = base_class_names + [
        f[0] for f in inspect.getmembers(base_list_classes, inspect.isclass)
    ]
    base_class_names = list(
        set(
            base_class_names
            + [
                f[0]
                for f in inspect.getmembers(base_list_indexed_classes, inspect.isclass)
            ]
        )
    )
    available_rules = []
    for module in modules:
        available_rules += [
            f
            for f in inspect.getmembers(
                module[1],
                lambda obj: inspect.isclass(obj)
                and issubclass(obj, RuleDefinitionBase),
            )
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
