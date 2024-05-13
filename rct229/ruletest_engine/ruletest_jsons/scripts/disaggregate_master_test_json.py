from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import (
    disaggregate_master_rmd_json,
    disaggregate_master_ruletest_json,
)

# Name of master spreadsheet in rct229.ruletest_engine.ruletest_jsons
json_name = "full_rpd_test_master.json"
output_dir = "full_rpds"
ruleset_doc = "ashrae9012019"
# disaggregate_master_ruletest_json(json_name, ruleset_doc)
disaggregate_master_rmd_json(json_name, output_dir, ruleset_doc)
