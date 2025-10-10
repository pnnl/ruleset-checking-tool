import importlib

from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore

# Add all available rule modules in __all__
__all__ = ["section5", "section6", "section21"]


rules_dict = {
    "PRM9012022Rule86r63": "section5rule43",
    "PRM9012022Rule13d92": "section5rule44",
    "PRM9012022Rule22f12": "section5rule45",
    "PRM9012022Rule12d80": "section6rule11",
    "PRM9012022Rule93e12": "section21rule19",
}

section_list = [
    "Env",
    "LTG",
    "HVAC-HotWaterSide",
]

section_dict = {
    "5": "Envelope",
    "6": "Lighting",
    "21": "HVAC-HotWaterSide",
}

# Update this field if 2022 uses different term.
if SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901"):
    RMD = SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901")
    COMMON_RMD = SchemaEnums.schema_enums.get("CommonRulesetModelOptions")

else:
    SchemaStore.set_ruleset(RuleSet.ASHRAE9012022_RULESET)
    SchemaEnums.update_schema_enum()
    RMD = SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901")
    COMMON_RMD = SchemaEnums.schema_enums.get("CommonRulesetModelOptions")

BASELINE_0 = RMD.BASELINE_0
BASELINE_90 = RMD.BASELINE_90
BASELINE_180 = RMD.BASELINE_180
BASELINE_270 = RMD.BASELINE_270
USER = COMMON_RMD.USER
PROPOSED = COMMON_RMD.PROPOSED


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
