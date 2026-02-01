from pathlib import Path


# Identify this ruleset’s root directory
ROOT_DIR = Path(__file__).parent

# Collect subdirectories (these correspond to ruletest sections)
RULETEST_SECTION_LIST = [
    p.name
    for p in ROOT_DIR.iterdir()
    if p.is_dir() and p.name not in ["ruletest_spreadsheets", "__pycache__"]
]
RULETEST_SECTION_LIST.sort()
