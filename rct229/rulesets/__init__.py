import importlib
import inspect

import rct229.rule_engine.partial_rule_definition as base_partial_rule_classes
import rct229.rule_engine.rule_base as base_classes
import rct229.rule_engine.rule_list_base as base_list_classes
import rct229.rule_engine.rule_list_indexed_base as base_list_indexed_classes
import rct229.rulesets as rulesets
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rulesets import RuleSet

# All list for registering a ruleset.
__all__ = [RuleSet.ASHRAE9012019_RULESET]

# Added to remove the sub-module that are not rules.
from rct229.schema.schema_store import SchemaStore

MODULE_EXCEPTION_LIST = ["math", "itertools"]


def __getrules__():
    modules = []
    ruleset_list = inspect.getmembers(rulesets, inspect.ismodule)
    for ruleset in ruleset_list:
        if ruleset[0] == SchemaStore.SELECTED_RULESET:
            __getrules_module__helper(ruleset[1], modules)
    # Adding the module names that should be excluded from the available rules. Such as RuleDefinitionBase
    base_class_names = [f[0] for f in inspect.getmembers(base_classes, inspect.isclass)]
    base_class_names = base_class_names + [
        f[0] for f in inspect.getmembers(base_list_classes, inspect.isclass)
    ]
    base_class_names = base_class_names + [
        f[0] for f in inspect.getmembers(base_partial_rule_classes, inspect.isclass)
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
    # --- End adding base class names
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


def __getrulemap__():
    ruleset_list = inspect.getmembers(rulesets, inspect.ismodule)
    for ruleset in ruleset_list:
        if ruleset[0] == SchemaStore.SELECTED_RULESET:
            rules_dict = getattr(ruleset[1], "rules_dict", None)
            return rules_dict


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
