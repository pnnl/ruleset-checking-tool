from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.assertions import getattr_
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

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
            each_rule=Section5Rule18.ZoneRule(),
            index_rmr=BASELINE_0,
            id="5-18",
            description="The baseline fenestration area for an existing building shall equal the existing "
                        "fenestration area prior to the proposed work.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*].zones[*]",
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
            return getattr_(zone_b, "zones", "spaces", "status_type") in [
                GENERAL_STATUS.EXISTING,
                GENERAL_STATUS.ALTERED,
            ]

        def get_calc_vals(self, context, data=None):
            zone_b = context.BASELINE_0
            undetermined_zone_list = find_all("$.spaces[*]", zone_b)
            return {"undetermined_zone_list": undetermined_zone_list}

        def applicability_check(self, context, calc_vals, data):
            undetermined_zone_list = calc_vals["undetermined_zone_list"]
            return undetermined_zone_list

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            undetermined_zone_list = calc_vals["undetermined_zone_list"]
            return (
                f"Part or all of zones listed below is existing or altered. The baseline vertical fenestration "
                f"area for existing zones must equal to the fenestration area prior to the proposed scope of "
                f"work. The baseline fenestration area in zone must be checked manually.{undetermined_zone_list}"
            )
