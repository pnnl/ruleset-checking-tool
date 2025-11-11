from pathlib import Path

section_rule_to_rule_id = {
    "6-11": f"{LIGHTING_DIR}-11",
    "6-12": f"{LIGHTING_DIR}-12",
    "21-19": f"{HVAC_HOT_WATER_DIR}-19",
}

# Identify this ruleset’s root directory
ROOT_DIR = Path(__file__).parent

# Collect subdirectories (these correspond to ruletest sections)
RULETEST_SECTION_LIST = [
    p.name
    for p in ROOT_DIR.iterdir()
    if p.is_dir() and p.name not in ["ruletest_spreadsheets", "__pycache__"]
]
RULETEST_SECTION_LIST.sort()
