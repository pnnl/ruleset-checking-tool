import importlib
import inspect
import sys
from importlib.metadata import entry_points

import rct229.rule_engine.partial_rule_definition as base_partial_rule_classes
import rct229.rule_engine.rule_base as base_classes
import rct229.rule_engine.rule_list_base as base_list_classes
import rct229.rule_engine.rule_list_indexed_base as base_list_indexed_classes
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_store import SchemaStore


MODULE_EXCEPTION_LIST = ["math", "itertools"]


# Dynamically load all registered rulesets via entry points
def discover_ruleset_plugins():
    eps = entry_points(group="rct229.rulesets")
    loaded = {}
    for ep in eps:
        try:
            mod = ep.load()
            loaded[ep.name] = mod
            setattr(sys.modules[__name__], ep.name, mod)
        except Exception as e:
            print(f"Warning: failed to load ruleset plugin '{ep.name}': {e}")
    return loaded


def register_rulesets():
    for name in __all__:
        setattr(RuleSet, name.upper().replace("-", "_") + "_RULESET", name)


# Dynamically discover all ruleset modules
_DISCOVERED_RULESETS = discover_ruleset_plugins()

# Update __all__ to reflect discovered rule names
__all__ = sorted(_DISCOVERED_RULESETS.keys())


def __getruleset__():
    selected = SchemaStore.SELECTED_RULESET
    return _DISCOVERED_RULESETS.get(selected)


def __getrules__():
    selected_ruleset = __getruleset__()
    if not selected_ruleset:
        return []

    modules = []
    __getrules_module__helper(selected_ruleset, modules)

    base_class_names = _get_base_class_names()

    available_rules = []
    for module in modules:
        available_rules += [
            f
            for f in inspect.getmembers(
                module[1],
                lambda obj: inspect.isclass(obj)
                and issubclass(obj, RuleDefinitionBase),
            )
            if not f[0].startswith("_") and f[0] not in base_class_names
        ]

    return available_rules


def __getrules_module__helper(rules, module_list):
    inspect_results = inspect.getmembers(rules, inspect.ismodule)
    for f in inspect_results:
        next_inspect_results = inspect.getmembers(f[1], inspect.ismodule)
        if len(next_inspect_results) == 0 or _meet_exception_modules(
            next_inspect_results
        ):
            module_list.append(f)
        else:
            __getrules_module__helper(f[1], module_list)


def _meet_exception_modules(inspection_results):
    """
    Function to make sure no module in the inspection results meets the exception list
    Parameters
    ----------
    inspection_results

    Returns
    -------

    """
    return any(f[0] in MODULE_EXCEPTION_LIST for f in inspection_results)


def _get_base_class_names():
    base_class_names = [f[0] for f in inspect.getmembers(base_classes, inspect.isclass)]
    base_class_names += [
        f[0] for f in inspect.getmembers(base_list_classes, inspect.isclass)
    ]
    base_class_names += [
        f[0] for f in inspect.getmembers(base_partial_rule_classes, inspect.isclass)
    ]
    base_class_names += [
        f[0] for f in inspect.getmembers(base_list_indexed_classes, inspect.isclass)
    ]
    return list(set(base_class_names))


def __getsectiondict__():
    selected_ruleset = __getruleset__()
    return getattr(selected_ruleset, "section_dict", None) if selected_ruleset else None


def __getrulemap__():
    selected_ruleset = __getruleset__()
    return getattr(selected_ruleset, "rules_dict", None) if selected_ruleset else None


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
