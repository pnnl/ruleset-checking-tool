import importlib
import pkgutil
import re
from pathlib import Path

from rct229.schema.schema_enums import SchemaEnums

# Add all available rule modules in __all__
__all__ = [
    "section5",
    "section6",
    "section21",
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
    "PRM9012022Rule86r63": "section5rule43",
    "PRM9012022Rule13d92": "section5rule44",
    "PRM9012022Rule22f12": "section5rule45",
    "PRM9012022Rule12d80": "section6rule11",
    "PRM9012022Rule93e12": "section21rule19",
}

section_list = [
    "All",
    "Envelope",
    "Lighting",
    "HVAC-HotWaterSide",
]

section_dict = {
    "5": "Envelope",
    "6": "Lighting",
    "21": "HVAC-HotWaterSide",
}

# Update this field if 2022 uses different term.
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
