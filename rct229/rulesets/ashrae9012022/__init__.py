import importlib

from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore

# Add all available rule modules in __all__
__all__ = ["section5", "section6", "section21"]

rules_dict = {
    "prm9012022rule77j30": "section5rule1",
    "prm9012022rule72a03": "section5rule2",
    "prm9012022rule73o42": "section5rule3",
    "prm9012022rule43n21": "section5rule4",
    "prm9012022rule02s62": "section5rule5",
    "prm9012022rule70u00": "section5rule6",
    "prm9012022rule20r05": "section5rule7",
    "prm9012022rule48v87": "section5rule8",
    "prm9012022rule38m70": "section5rule9",
    "prm9012022rule29j06": "section5rule10",
    "prm9012022rule46p73": "section5rule11",
    "prm9012022rule40d86": "section5rule12",
    "prm9012022rule73r04": "section5rule13",
    "prm9012022rule67j71": "section5rule14",
    "prm9012022rule04o58": "section5rule15",
    "prm9012022rule80o45": "section5rule16",
    "prm9012022rule87g56": "section5rule17",
    "prm9012022rule82y74": "section5rule18",
    "prm9012022rule57c26": "section5rule19",
    "prm9012022rule96n40": "section5rule20",
    "prm9012022rule44m70": "section5rule21",
    "prm9012022rule50p59": "section5rule22",
    "prm9012022rule11q41": "section5rule23",
    "prm9012022rule78j13": "section5rule24",
    "prm9012022rule84u02": "section5rule25",
    "prm9012022rule34b75": "section5rule26",
    "prm9012022rule69v04": "section5rule27",
    "prm9012022rule42c42": "section5rule28",
    "prm9012022rule39f24": "section5rule29",
    "prm9012022rule18s99": "section5rule30",
    "prm9012022rule48w84": "section5rule31",
    "prm9012022rule78r30": "section5rule32",
    "prm9012022rule45p36": "section5rule33",
    "prm9012022rule69u47": "section5rule34",
    "prm9012022rule39k65": "section5rule35",
    "prm9012022rule23m90": "section5rule36",
    "prm9012022rule67a77": "section5rule37",
    "prm9012022rule40i28": "section5rule38",
    "prm9012022rule50m61": "section5rule39",
    "prm9012022rule33l08": "section5rule40",
    "prm9012022rule49t86": "section5rule42",
    "prm9012022rule86r63": "section5rule43",
    "prm9012022rule13d92": "section5rule44",
    "prm9012022rule22f12": "section5rule45",
    "prm9012022rule12d80": "section6rule11",
    "prm9012022rule93e12": "section21rule19",

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
