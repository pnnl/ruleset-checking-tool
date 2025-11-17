from rct229.ruletest_engine.ruletest_jsons.scripts.excel_generation_utilities import (
    create_rule_test_documentation_spreadsheet,
)
from rct229.schema.schema_store import SchemaStore
from rct229.rule_engine.rulesets import RuleSet


# INPUT:
ruleset_standard = RuleSet.ASHRAE9012019_RULESET
SchemaStore.set_ruleset(ruleset_standard)
test_json_branch = "public_review_2nd"

# Create rule test documentation for ruleset standard specified above
create_rule_test_documentation_spreadsheet(test_json_branch)
