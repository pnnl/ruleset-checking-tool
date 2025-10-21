from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore
from rct229.rule_engine.rulesets import RuleSet
from rct229.ruletest_engine.ruletest_jsons.scripts.json_generation_utilities import (
    disaggregate_master_rmd_json,
    disaggregate_master_ruletest_json,
)

# --- SELECT A RULESET ---
# ruleset = RuleSet.ASHRAE9012019_RULESET
ruleset = RuleSet.ASHRAE9012022_RULESET

# --- SET THE MASTER JSON FILENAME TO DISAGGREGATE ---
json_name = "section5_envelope_tcd_2022.json"


SchemaStore.set_ruleset(ruleset)
SchemaEnums.update_schema_enum()
disaggregate_master_ruletest_json(json_name, ruleset)

# --- SET THE OUTPUT DIRECTORY ---
# output_dir = "system_types"

# disaggregate_master_rmd_json(json_name, output_dir, ruleset_doc)
