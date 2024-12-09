import importlib

from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore

# Add all available rule modules in __all__
__all__ = [
    "section1",
    "section4",
    "section5",
    "section6",
    "section10",
    "section11",
    "section12",
    "section16",
    "section18",
    "section19",
    "section21",
    "section22",
    "section23",
]

if SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901"):
    RMT = SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901")
else:
    SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
    SchemaEnums.update_schema_enum()
    RMT = SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901")

BASELINE_0 = RMT.BASELINE_0
BASELINE_90 = RMT.BASELINE_90
BASELINE_180 = RMT.BASELINE_180
BASELINE_270 = RMT.BASELINE_270
USER = RMT.USER
PROPOSED = RMT.PROPOSED


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
