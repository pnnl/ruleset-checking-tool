from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

GENERAL_STATUS = SchemaEnums.schema_enums["SpaceStatusOptions2019ASHRAE901"]

APPLICABLE_GENERAL_STATUS = [
    GENERAL_STATUS.EXISTING,
    GENERAL_STATUS.ALTERED,
]


class Section5Rule18(PartialRuleDefinition):
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
            rmr_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0

        return any(
            [
                status_type_b in APPLICABLE_GENERAL_STATUS
                for status_type_b in find_all("$.spaces[*].status_type", rmd_b)
            ]
        )

    def get_calc_vals(self, context, data=None):
        rmd_b = context.BASELINE_0

        undetermined_zone_list_b = [
            zone_b["id"]
            for zone_b in find_all(
                "$.buildings[*].building_segments[*].zones[*]", rmd_b
            )
            for status_type_b in find_all("spaces[*].status_type", zone_b)
            if status_type_b in APPLICABLE_GENERAL_STATUS
        ]

        return {"undetermined_zone_list_b": undetermined_zone_list_b}

    def applicability_check(self, context, calc_vals, data):
        undetermined_zone_list_b = calc_vals["undetermined_zone_list_b"]

        return bool(undetermined_zone_list_b)

    def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
        undetermined_zone_list_b = calc_vals["undetermined_zone_list_b"]

        return (
            f"Part or all of zones listed below is existing or altered. The baseline vertical fenestration "
            f"area for existing zones must equal to the fenestration area prior to the proposed scope of "
            f"work. The baseline fenestration area in zone must be checked manually.{undetermined_zone_list_b}"
        )
