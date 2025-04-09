from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

GENERAL_STATUS = SchemaEnums.schema_enums["StatusOptions"]

APPLICABLE_GENERAL_STATUS = [
    GENERAL_STATUS.EXISTING,
    GENERAL_STATUS.ALTERED,
]


class PRM9012019Rule87g56(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule87g56, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="5-17",
            description="The baseline fenestration area for an existing building shall equal the existing "
            "fenestration area prior to the proposed work.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=False,
            each_rule=PRM9012019Rule87g56.ZoneRule(),
            index_rmd=BASELINE_0,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*].zones[*]",
        )

    class ZoneRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule87g56.ZoneRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def is_applicable(self, context, data=None):
            zone_b = context.BASELINE_0
            return any(
                [
                    status_type_b in APPLICABLE_GENERAL_STATUS
                    for status_type_b in find_all("$.spaces[*].status_type", zone_b)
                ]
            )

        def get_calc_vals(self, context, data=None):
            zone_b = context.BASELINE_0

            existing_or_altered_space_list_b = [
                space_b["id"]
                for space_b in find_all("$.spaces[*]", zone_b)
                if space_b.get("status_type") in APPLICABLE_GENERAL_STATUS
            ]

            return {
                "existing_or_altered_space_list_b": existing_or_altered_space_list_b
            }

        def applicability_check(self, context, calc_vals, data):
            existing_or_altered_space_list_b = calc_vals[
                "existing_or_altered_space_list_b"
            ]

            return len(existing_or_altered_space_list_b) > 0

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            existing_or_altered_space_list_b = calc_vals[
                "existing_or_altered_space_list_b"
            ]

            return f"Part or all of spaces listed below is existing or altered. The baseline vertical fenestration area for a existing zone must equal to the fenestration area prior to the proposed scope of work. The baseline fenestration area in zone must be checked manually. ${existing_or_altered_space_list_b}"
