import importlib
import pkgutil
import re
from pathlib import Path

from rct229.schema.schema_enums import SchemaEnums

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
    "section_list",
    "section_dict",
    "SHORT_NAME",
    "BASELINE_0",
    "BASELINE_90",
    "BASELINE_180",
    "BASELINE_270",
    "USER",
    "PROPOSED",
]

SHORT_NAME = "prm9012022"

rules_dict = {
    "prm9012022rule73j65": "section1rule1",
    "prm9012022rule63e94": "section1rule2",
    "prm9012022rule88z11": "section1rule3",
    "prm9012022rule60m79": "section1rule4",
    "prm9012022rule86h31": "section1rule5",
    "prm9012022rule10d53": "section1rule6",
    "prm9012022rule37e66": "section1rule7",
    "prm9012022rule71o26": "section1rule8",
    "prm9012022rule51z38": "section1rule9",
    "prm9012022rule96q77": "section4rule1",
    "prm9012022rule85i93": "section4rule2",
    "prm9012022rule18y74": "section4rule11",
    "prm9012022rule66c61": "section4rule14",
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
    "prm9012022Rule82e93": "section5rule42",
    "prm9012022Rule86r63": "section5rule43",
    "prm9012022Rule13d92": "section5rule44",
    "prm9012022Rule22f12": "section5rule45",
    "prm9012022rule99c05": "section6rule1",
    "prm9012022rule37d98": "section6rule2",
    "prm9012022rule73a47": "section6rule3",
    "prm9012022rule22l93": "section6rule4",
    "prm9012022rule08a45": "section6rule5",
    "prm9012022rule02c29": "section6rule6",
    "prm9012022rule66m62": "section6rule7",
    "prm9012022rule16x33": "section6rule8",
    "prm9012022rule22c86": "section6rule9",
    "prm9012022Rule23o29": "section6rule11",
    "prm9012022Rule12d80": "section6rule12",
    "prm9012022rule86d29": "section6rule13",
    "prm9012022rule86j27": "section10rule1",
    "prm9012022rule34l50": "section10rule7",
    "prm9012022rule73m45": "section10rule10",
    "prm9012022rule10p28": "section10rule14",
    "prm9012022rule93u32": "section10rule15",
    "prm9012022rule72v93": "section11rule1",
    "prm9012022rule23f92": "section11rule5",
    "prm9012022rule29n09": "section11rule6",
    "prm9012022rule49y39": "section11rule7",
    "prm9012022rule40i48": "section11rule8",
    "prm9012022rule93n40": "section11rule9",
    "prm9012022rule76q85": "section11rule10",
    "prm9012022rule29i55": "section11rule11",
    "prm9012022rule52y79": "section11rule12",
    "prm9012022rule51s51": "section11rule13",
    "prm9012022rule62z26": "section11rule14",
    "prm9012022rule06k20": "section11rule15",
    "prm9012022rule23k17": "section11rule16",
    "prm9012022rule63z32": "section11rule17",
    "prm9012022rule88h78": "section12rule1",
    "prm9012022rule66e91": "section12rule2",
    "prm9012022rule79w60": "section12rule3",
    "prm9012022rule60e48": "section12rule4",
    "prm9012022rule73v23": "section12rule5",
    "prm9012022rule98t42": "section16rule1",
    "prm9012022rule66a48": "section16rule2",
    "prm9012022rule92n36": "section16rule3",
    "prm9012022rule03a79": "section16rule4",
    "prm9012022rule55z67": "section16rule5",
    "prm9012022rule34h06": "section16rule6",
    "prm9012022rule30t80": "section16rule7",
    "prm9012022rule77j55": "section18rule1",
    "prm9012022rule51v53": "section18rule2",
    "prm9012022rule00u91": "section18rule3",
    "prm9012022rule73r44": "section19rule1",
    "prm9012022rule93f21": "section19rule2",
    "prm9012022rule16j07": "section19rule3",
    "prm9012022rule74p61": "section19rule4",
    "prm9012022rule75k92": "section19rule5",
    "prm9012022rule97a53": "section19rule6",
    "prm9012022rule29n92": "section19rule7",
    "prm9012022rule02h13": "section19rule8",
    "prm9012022rule23q51": "section19rule9",
    "prm9012022rule76q46": "section19rule10",
    "prm9012022rule18u58": "section19rule11",
    "prm9012022rule98o22": "section19rule12",
    "prm9012022rule77j17": "section19rule13",
    "prm9012022rule60f12": "section19rule14",
    "prm9012022rule03j97": "section19rule15",
    "prm9012022rule04f07": "section19rule16",
    "prm9012022rule84b07": "section19rule17",
    "prm9012022rule49c09": "section19rule18",
    "prm9012022rule51d17": "section19rule19",
    "prm9012022rule60d49": "section19rule20",
    "prm9012022rule07w16": "section19rule21",
    "prm9012022rule44t17": "section19rule22",
    "prm9012022rule60o81": "section19rule23",
    "prm9012022rule54e25": "section19rule24",
    "prm9012022rule10q01": "section19rule25",
    "prm9012022rule09g49": "section19rule26",
    "prm9012022rule88f26": "section19rule27",
    "prm9012022rule20g60": "section19rule28",
    "prm9012022rule20z34": "section19rule29",
    "prm9012022rule95r49": "section19rule30",
    "prm9012022rule58x03": "section19rule31",
    "prm9012022rule31y73": "section19rule32",
    "prm9012022rule28i68": "section19rule33",
    "prm9012022rule87f72": "section19rule34",
    "prm9012022rule40n43": "section19rule35",
    "prm9012022rule45j93": "section19rule36",
    "prm9012022rule86o02": "section19rule37",
    "prm9012022rule34f57": "section21rule1",
    "prm9012022rule83m55": "section21rule2",
    "prm9012022rule86n98": "section21rule3",
    "prm9012022rule63n48": "section21rule4",
    "prm9012022rule34r52": "section21rule5",
    "prm9012022rule47b05": "section21rule6",
    "prm9012022rule92f56": "section21rule7",
    "prm9012022rule58s22": "section21rule8",
    "prm9012022rule39a29": "section21rule9",
    "prm9012022rule06a67": "section21rule10",
    "prm9012022rule59p62": "section21rule11",
    "prm9012022rule22a24": "section21rule12",
    "prm9012022rule43l11": "section21rule13",
    "prm9012022rule29g28": "section21rule14",
    "prm9012022rule62u16": "section21rule15",
    "prm9012022rule31d63": "section21rule16",
    "prm9012022rule35d81": "section21rule17",
    "prm9012022rule82a90": "section21rule18",
    "prm9012022Rule93e12": "section21rule19",
    "prm9012022rule92r39": "section22rule1",
    "prm9012022rule59b18": "section22rule2",
    "prm9012022rule58a51": "section22rule3",
    "prm9012022rule13x50": "section22rule4",
    "prm9012022rule38u90": "section22rule5",
    "prm9012022rule52t53": "section22rule6",
    "prm9012022rule52s13": "section22rule7",
    "prm9012022rule37a05": "section22rule8",
    "prm9012022rule78g49": "section22rule9",
    "prm9012022rule41z21": "section22rule10",
    "prm9012022rule57w94": "section22rule11",
    "prm9012022rule99f07": "section22rule12",
    "prm9012022rule92d16": "section22rule13",
    "prm9012022rule95f90": "section22rule14",
    "prm9012022rule79g01": "section22rule15",
    "prm9012022rule81f32": "section22rule16",
    "prm9012022rule04g06": "section22rule17",
    "prm9012022rule38d92": "section22rule18",
    "prm9012022rule68h16": "section22rule19",
    "prm9012022rule71o81": "section22rule20",
    "prm9012022rule96z66": "section22rule21",
    "prm9012022rule55f82": "section22rule22",
    "prm9012022rule67l25": "section22rule23",
    "prm9012022rule47d94": "section22rule24",
    "prm9012022rule03q09": "section22rule25",
    "prm9012022rule18j38": "section22rule26",
    "prm9012022rule86p62": "section22rule27",
    "prm9012022rule41d32": "section22rule28",
    "prm9012022rule60w01": "section22rule29",
    "prm9012022rule79u84": "section22rule30",
    "prm9012022rule30m88": "section22rule31",
    "prm9012022rule48s83": "section22rule32",
    "prm9012022rule88r57": "section22rule33",
    "prm9012022rule36t85": "section22rule34",
    "prm9012022rule20a97": "section22rule35",
    "prm9012022rule01b91": "section22rule36",
    "prm9012022rule81j88": "section22rule37",
    "prm9012022rule84g72": "section22rule38",
    "prm9012022rule33w37": "section22rule39",
    "prm9012022rule48h16": "section22rule40",
    "prm9012022rule68r93": "section22rule41",
    "prm9012022Rule34d03": "section22rule42",
    "prm9012022Rule93e20": "section22rule43",
    "prm9012022Rule43f22": "section22rule44",
    "prm9012022rule79m01": "section23rule1",
    "prm9012022rule52x31": "section23rule2",
    "prm9012022rule44u85": "section23rule3",
    "prm9012022rule68z84": "section23rule4",
    "prm9012022rule69z86": "section23rule5",
    "prm9012022rule98g04": "section23rule6",
    "prm9012022rule62j00": "section23rule7",
    "prm9012022rule45r08": "section23rule8",
    "prm9012022rule46w18": "section23rule9",
    "prm9012022rule18u93": "section23rule10",
    "prm9012022rule47f22": "section23rule11",
    "prm9012022rule71k98": "section23rule12",
    "prm9012022rule50v48": "section23rule13",
    "prm9012022rule14m33": "section23rule14",
    "prm9012022rule71f87": "section23rule15",
    "prm9012022rule79i34": "section23rule16",
    "prm9012022rule40y63": "section23rule17",
}

section_list = [
    "All",
    "Performance Calculations",
    "Schedules Setpoints",
    "Envelope",
    "Lighting",
    "HVAC General",
    "Service Hot Water",
    "Receptacles",
    "Transformers",
    "Elevator",
    "HVAC-Baseline",
    "HVAC-General",
    "HVAC-HotWaterSide",
    "HVAC-ChilledWaterSide",
    "HVAC-AirSide",
]

section_dict = {
    "1": "Performance Calculations",
    "4": "Schedules Setpoints",
    "5": "Envelope",
    "6": "Lighting",
    "10": "HVAC General",
    "11": "Service Hot Water",
    "12": "Receptacles",
    "16": "Elevator",
    "18": "HVAC-Baseline",
    "19": "HVAC-General",
    "21": "HVAC-HotWaterSide",
    "22": "HVAC-ChilledWaterSide",
    "23": "HVAC-AirSide",
}

# Update this field if 2022 uses different term.
SchemaEnums.update_schema_enum_by_ruleset("ashrae9012022")
RMD = SchemaEnums.schema_enums.get("RulesetModelOptions2019ASHRAE901")
COMMON_RMD = SchemaEnums.schema_enums.get("CommonRulesetModelOptions")

BASELINE_0 = RMD.BASELINE_0
BASELINE_90 = RMD.BASELINE_90
BASELINE_180 = RMD.BASELINE_180
BASELINE_270 = RMD.BASELINE_270
USER = COMMON_RMD.USER
PROPOSED = COMMON_RMD.PROPOSED


def build_section_rule_to_rule_id(ruleset_package):
    """
    Dynamically generate a mapping of section-rule to rule ID using SHORT_NAME
    defined in each section's __init__.py.

    Example output:
    {
        "1-1": "CALC-1",
        "1-2": "CALC-2",
        "5-1": "ENV-1",
        ...
    }
    """
    section_number_to_name_map = {}

    # Iterate over all submodules/subpackages in the ruleset package (e.g., section1, section5)
    package_path = Path(ruleset_package.__path__[0])

    for finder, name, ispkg in pkgutil.iter_modules([str(package_path)]):
        if not name.startswith("section"):
            continue  # skip non-section directories

        section_module = importlib.import_module(f"{ruleset_package.__name__}.{name}")
        section_num_match = re.match(r"section(\d+)", name)
        if not section_num_match:
            continue

        # Get the SHORT_NAME defined in section's __init__.py
        short_name = getattr(section_module, "SHORT_NAME", None)
        if short_name is None:
            print(
                f"Warning: {name} missing SHORT_NAME in the __init__.py file. Skipping."
            )
            continue

        # Find all rule files (sectionXruleY.py)
        rule_files = [
            f
            for f in (package_path / name).glob("section*rule*.py")
            if re.match(r"section\d+rule\d+\.py$", f.name)
        ]

        for rule_file in rule_files:
            rule_match = re.match(r"section(\d+)rule(\d+)\.py$", rule_file.name)
            if rule_match:
                rule_section = rule_match.group(1)
                rule_num = rule_match.group(2)
                key = f"{rule_section}-{rule_num}"
                section_number_to_name_map[key] = f"{short_name}-{rule_num}"

    return section_number_to_name_map


# Automatically build the section-rule ID map when the package is imported
section_rule_to_rule_id = build_section_rule_to_rule_id(
    importlib.import_module(__name__)
)


def __getattr__(name):
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__)
