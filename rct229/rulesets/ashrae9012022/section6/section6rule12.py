from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import PROPOSED
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
LIGHTING_PURPOSE = SchemaEnums.schema_enums["LightingPurposeOptions2019ASHRAE901"]

MANUAL_CHECK_REQUIRED_MSG = (
    "It could not be determined whether the proposed retail display lighting power is less "
    "than or equal to the allowance calculated according to the formulas in ASHRAE 90.1 "
    "Section 9.5.2.2(b)."
)


class PRM9012022Rule12d80(RuleDefinitionListIndexedBase):
    """Rule 12 of ASHRAE 90.1-2022 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012022Rule12d80, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012022Rule12d80.SpaceRule(),
            index_rmd=PROPOSED,
            id="6-12",
            description="Where retail display lighting is included in the proposed building design the display lighting"
            "additional power shall be less than or equal to the limits established by Section 9.5.2.2(b) ",
            ruleset_section_title="Lighting",
            standard_section="G1.2.1b.1 and the methodology described in Table 9.5.2.2(b)",
            is_primary_rule=True,
            list_path="$.buildings[*].building_segments[*].zones[*].spaces[*]",
            rmd_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmd_p = context.PROPOSED

        return any(
            interior_lighting_p.get("purpose_type") == LIGHTING_PURPOSE.RETAIL_DISPLAY
            for space_p in find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*]", rmd_p
            )
            if space_p.get("lighting_space_type") == LIGHTING_SPACE.SALES_AREA
            for interior_lighting_p in space_p.get("interior_lighting", [])
        )

    class SpaceRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022Rule12d80.SpaceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={
                    "$": ["floor_area", "interior_lighting"],
                    "interior_lighting[*]": ["purpose_type", "power_per_area"],
                },
                precision={
                    "minimum_retail_display_W": {
                        "precision": 1,
                        "unit": "W",
                    },
                    "maximum_retail_display_W": {
                        "precision": 1,
                        "unit": "W",
                    },
                },
                manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
            )

        def get_calc_vals(self, context, data=None):
            space_p = context.PROPOSED

            # 9.5.2.2(b) gives a formula
            # 750 W + (Retail Area 1 × 0.40 W/ft2) + (Retail Area 2 × 0.40 W/ft2) + (Retail Area 3 × 0.70 W/ft2) + (Retail Area 4 × 1.00 W/ft2)
            # for retail display lighting that is based on four area categories.
            # We don't have access to these four area categories in the schema, so we will calculate the maximum and minimum values possible based on this function.
            # The maximum is calculated based on 100% of the space floor area being type 4: `maximum_retail_display_W = 750 + space.floor_area * (1)
            maximum_retail_display_W = 750 * ureg("W") + space_p["floor_area"].to(
                "ft2"
            ) * 1.0 * ureg("W/ft2")
            minimum_retail_display_W = 750 * ureg("W")
            proposed_interior_display_W = sum(
                [
                    interior_lighting_p["power_per_area"] * space_p["floor_area"]
                    for interior_lighting_p in space_p["interior_lighting"]
                    if interior_lighting_p["purpose_type"]
                    == LIGHTING_PURPOSE.RETAIL_DISPLAY
                ]
            )
            return {
                "maximum_retail_display_W": maximum_retail_display_W,
                "minimum_retail_display_W": minimum_retail_display_W,
                "proposed_interior_display_W": proposed_interior_display_W,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            maximum_retail_display_W = calc_vals["maximum_retail_display_W"]
            minimum_retail_display_W = calc_vals["minimum_retail_display_W"]
            proposed_interior_display_W = calc_vals["proposed_interior_display_W"]

            return (
                minimum_retail_display_W < proposed_interior_display_W
                or self.precision_comparison["minimum_retail_display_W"](
                    proposed_interior_display_W, minimum_retail_display_W
                )
            ) and (
                proposed_interior_display_W < maximum_retail_display_W
                or self.precision_comparison["maximum_retail_display_W"](
                    proposed_interior_display_W, maximum_retail_display_W
                )
            )

        def rule_check(self, context, calc_vals=None, data=None):
            minimum_retail_display_W = calc_vals["minimum_retail_display_W"]
            proposed_interior_display_W = calc_vals["proposed_interior_display_W"]

            return proposed_interior_display_W < minimum_retail_display_W
