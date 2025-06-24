from rct229.ruletest_engine.ruletest_jsons.scripts.excel_generation_utilities import (
    create_rule_test_documentation_spreadsheet,
)

# INPUT:
ruleset_standard = "ashrae9012019"
test_json_branch = "RT/JG/schema_update_016_017"

# Create rule test documentation for ruleset standard specified above
create_rule_test_documentation_spreadsheet(ruleset_standard, test_json_branch)
