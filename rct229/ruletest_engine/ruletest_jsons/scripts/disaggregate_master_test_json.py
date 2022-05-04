from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import (
    disaggregate_master_ruletest_json,
)

# Name of master spreadsheet in rct229.ruletest_engine.ruletest_jsons
json_name = "envelope_tests.json"

disaggregate_master_ruletest_json(json_name)
