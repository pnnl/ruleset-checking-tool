import os

from rct229.schema.schema_store import SchemaStore
from rct229.rule_engine.rulesets import RuleSet
from rct229.ruletest_engine.ruletest_engine import validate_test_json_schema
from rct229.ruletest_engine.ruletest_jsons.scripts.excel_to_test_json_utilities import (
    create_test_json_from_excel,
    update_unit_convention_record,
)

# ---------------------------------------USER INPUTS---------------------------------------

# Excel to master test JSON inputs
spreadsheet_name = "section5_envelope_tcd_2022.xlsx"
test_json_name = "section5_envelope_tcd_2022.json"
sheet_name = "TCDs"

# Flag to determine if you should check the test JSON
check_schema = False

# --- SELECT A RULESET ---
# ruleset = RuleSet.ASHRAE9012019_RULESET
rule_set = RuleSet.ASHRAE9012022_RULESET

# --------------------------------------SCRIPT STARTS--------------------------------------

SchemaStore.set_ruleset(rule_set)
# Create a test JSON for a given ruletest spreadsheet
create_test_json_from_excel(spreadsheet_name, sheet_name, test_json_name, rule_set)

# Parse ruletest spreadsheet for unit types and update the unit conventions in unit_convention.json for:
# -RMD (typically SI)
# -Rule Tests (typically IP)
update_unit_convention_record(spreadsheet_name, sheet_name, rule_set)

# Check generated master JSON against latest schema
json_dir = os.path.join(os.path.dirname(__file__), "..", rule_set)
test_json_path = os.path.join(json_dir, test_json_name)

if check_schema:
    validate_test_json_schema(test_json_path)
