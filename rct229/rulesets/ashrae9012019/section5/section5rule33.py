from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

CONSTANT = SchemaEnums.schema_enums["InfiltrationMethodOptions"].CONSTANT


class PRM9012019Rule45p36(RuleDefinitionListIndexedBase):
    """Rule 33 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule45p36, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule45p36.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-33",
            description="The infiltration modeling method in the baseline includes adjustment for weather and building operation.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule45p36.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$.building_segments[*].zones[*].spaces[*].infiltration": [
                        "modeling_method"
                    ]
                },
            )

        def get_calc_vals(self, context, data=None):
            baseline_infiltration = find_all(
                "$.building_segments[*].zones[*].infiltration", context.BASELINE_0
            )
            failing_infiltration_ids = [
                b_infiltration["id"]
                for b_infiltration in baseline_infiltration
                if b_infiltration["modeling_method"] == CONSTANT
            ]
            return {"failing_infiltration_ids": failing_infiltration_ids}

        def rule_check(self, context, calc_vals=None, data=None):
            return len(calc_vals["failing_infiltration_ids"]) == 0
