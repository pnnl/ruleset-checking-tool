import os

from rct229.ruletest_engine.ruletest_engine import validate_test_json_schema
from rct229.ruletest_engine.ruletest_jsons.scripts.excel_to_test_json_utilities import (
    create_test_json_from_excel,
    update_unit_convention_record,
)
from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import (
    disaggregate_master_ruletest_json,
)

# ---------------------------------------USER INPUTS---------------------------------------

sheet_name = "TCDs"

# Flag to determine if you should check the test JSON's schema
check_schema = False

# The rule set being evaluated (e.g., 'ashrae902019'). Should correspond to a directory name in ruletests_jsons
rule_set = "ashrae9012019"

from rct229.ruletest_engine.ruletest_jsons.ashrae9012019 import *

spreadsheet_to_category_mapping = {
    "section1_performance_calc_tcd_renumb": PERFORMANCE_CALC_DIR,
    "section4_setpoint_tcd_renumb": SCHEDULE_DIR,
    "section5_envelope_tcd_renumb": ENVELOPE_DIR,
    "section6_lighting_tcd_renumb": LIGHTING_DIR,
    "section10_general_hvac_tcd_renumb": HVAC_GENERAL_DIR,
    "section11_service_hot_water_tcd_renumb": SERVICE_HOT_WATER_DIR,
    "section12_receptacle_tcd_renumb": RECEPTACLE_DIR,
    "section16_elevators_tcd_renumb": ELEVATOR_DIR,
    "section18_system_zone_assignment_tcd_renumb": HVAC_BASELINE_DIR,
    "section19_hvac_airside_tcd_renumb": HVAC_GENERAL_DIR,
    "section21_boiler_tcd_renumb": HVAC_HOT_WATER_DIR,
    "section22_chiller_tcd_renumb": HVAC_CHILLED_WATER_DIR,
    "section23_airside_hvac_tcd_renumb": HVAC_AIRSIDE_DIR,
}


# --------------------------------------SCRIPT STARTS--------------------------------------

# Iterate through spreadsheet to category mapping and generate JSONs
for (
    section_ruletest_spreadsheet,
    category_name,
) in spreadsheet_to_category_mapping.items():
    spreadsheet_name = f"{section_ruletest_spreadsheet}.xlsx"
    test_json_name = f"{section_ruletest_spreadsheet}.json"

    # Create test JSON
    create_test_json_from_excel(spreadsheet_name, sheet_name, test_json_name)

    # Update unit conventions
    update_unit_convention_record(spreadsheet_name, sheet_name)

    # Validate test JSON schema if flag is set
    json_dir = os.path.join(os.path.dirname(__file__), "..", rule_set)
    test_json_path = os.path.join(json_dir, test_json_name)

    if check_schema:
        validate_test_json_schema(test_json_path)

    # Disaggregate master JSON
    master_json_name = test_json_name
    disaggregate_master_ruletest_json(master_json_name, rule_set, category_name)
