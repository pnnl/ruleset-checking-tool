import importlib
from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore


# Add all available rule modules in __all__
__all__ = []

# Update this field if 2022 uses different term.
if SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901"):
    RMD = SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901")
else:
    SchemaStore.set_ruleset(RuleSet.ASHRAE9012022_RULESET)
    SchemaEnums.update_schema_enum()
    RMD = SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901")

BASELINE_0 = RMD.BASELINE_0
BASELINE_90 = RMD.BASELINE_90
BASELINE_180 = RMD.BASELINE_180
BASELINE_270 = RMD.BASELINE_270
USER = RMD.USER
PROPOSED = RMD.PROPOSED


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
