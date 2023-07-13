from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_all

CONSTANT = schema_enums["InfiltrationMethodOptions"].CONSTANT


class Section5Rule44(RuleDefinitionListIndexedBase):
    """Rule 44 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule44, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule44.BuildingRule(),
            index_rmr="baseline",
            id="5-44",
            description="The infiltration modeling method in the baseline includes adjustment for weather and building operation.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule44.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={"$..infiltration": ["modeling_method"]},
            )

        def get_calc_vals(self, context, data=None):
            baseline_infiltration = find_all("$..infiltration", context.baseline)
            failing_infiltration_ids = [
                b_infiltration["id"]
                for b_infiltration in baseline_infiltration
                if b_infiltration["modeling_method"] == CONSTANT
            ]
            return {"failing_infiltration_ids": failing_infiltration_ids}

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["failing_infiltration_ids"]) == 0
