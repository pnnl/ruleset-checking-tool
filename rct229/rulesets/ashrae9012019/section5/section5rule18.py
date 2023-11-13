from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.rulesets.ashrae9012019 import BASELINE_0

GENERAL_STATUS = SchemaEnums.schema_enums["SpaceStatusOptions2019ASHRAE901"]

APPLICABLE_GENERAL_STATUS = [
    GENERAL_STATUS.EXISTING,
    GENERAL_STATUS.ALTERED,
]


class Section5Rule18(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule18, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="5-18",
            description="The baseline fenestration area for an existing building shall equal the existing "
            "fenestration area prior to the proposed work.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=False,
            each_rule=Section5Rule18.ZoneRule(),
            index_rmr=BASELINE_0,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].zones[*]",
        )

    class ZoneRule(PartialRuleDefinition):
        def __init__(self):
            super(Section5Rule18.ZoneRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
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

            has_existing_or_altered_space = any(
                [
                    space_b["id"]
                    for space_b in find_all("$.spaces[*]", zone_b)
                    if space_b.get("status_type") in APPLICABLE_GENERAL_STATUS
                ]
            )

            return {"has_existing_or_altered_space": has_existing_or_altered_space}

        def applicability_check(self, context, calc_vals, data):
            has_existing_or_altered_space = calc_vals["has_existing_or_altered_space"]

            return has_existing_or_altered_space

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            has_existing_or_altered_space = calc_vals["has_existing_or_altered_space"]

            return (
                f"Part or all of zones listed below is existing or altered. The baseline vertical fenestration "
                f"area for existing zones must equal to the fenestration area prior to the proposed scope of "
                f"work. The baseline fenestration area in zone must be checked manually.{has_existing_or_altered_space}"
            )
