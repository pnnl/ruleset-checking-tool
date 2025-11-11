from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import BASELINE_0
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

LIGHTING_PURPOSE = SchemaEnums.schema_enums["LightingPurposeOptions2019ASHRAE901"]

MANUAL_CHECK_REQUIRED_MSG = (
    "It could not be determined whether the baseline retail display lighting power is modeled correctly "
    "as the minimum of the proposed retail display lighting power and the allowance calculated according to the formulas in ASHRAE 90.1 Section 9.5.2.2(b)."
)


class PRM9012022Rule23o29(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2022 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012022Rule23o29, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012022Rule23o29.BuildingRule(),
            index_rmd=BASELINE_0,
            id="6-11",
            description="Where retail display lighting is included in the proposed building design in accordance with Section 9.5.2.2(b), "
            "the baseline building design retail display lighting additional power shall be equal to the limits established by Section 9.5.2.2(b) or same as proposed, whichever is less.",
            ruleset_section_title="Lighting",
            standard_section="G3.1 #6 Baseline column",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012022Rule23o29.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012022Rule23o29.BuildingRule.SpaceRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].spaces[*]",
            )

        def is_applicable(self, context, data=None):
            building_p = context.PROPOSED

            return len(
                find_all(
                    "$.building_segments[*].zones[*].spaces[*].interior_lighting[*]",
                    building_p,
                )
            ) > 0 and any(
                [
                    interior_lighting.get("purpose_type")
                    == LIGHTING_PURPOSE.RETAIL_DISPLAY
                    for interior_lighting in find_all(
                        "$.building_segments[*].zones[*].spaces[*].interior_lighting[*]",
                        building_p,
                    )
                ]
            )

        def list_filter(self, context_item, data):
            space_p = context_item.PROPOSED

            return space_p.get("interior_lighting")

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012022Rule23o29.BuildingRule.SpaceRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    precision={
                        "minimum_retail_display_w": {
                            "precision": 1,
                            "unit": "W",
                        },
                        "baseline_interior_display_w": {
                            "precision": 1,
                            "unit": "W",
                        },
                    },
                    manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
                )

            def get_calc_vals(self, context, data=None):
                space_b = context.BASELINE_0
                space_p = context.PROPOSED

                # 9.5.2.2(b) gives a formula
                # (750 W + (Retail Area 1 × 0.40 W/ft2) + (Retail Area 2 × 0.40 W/ft2) + (Retail Area 3 × 0.70 W/ft2) + (Retail Area 4 × 1.00 W/ft2))
                # for retail display lighting that is based on four area categories.
                # We don't have access to these four area categories in the schema, so we will calculate the maximum and minimum values possible based on this function.

                maximum_retail_display_w = 750 * ureg("W") + space_p["floor_area"].to(
                    "ft2"
                ) * 1.0 * ureg("W/ft2")
                minimum_retail_display_w = 750 * ureg("W")

                baseline_interior_display_w = sum(
                    [
                        interior_lighting_b.get("power_per_area", 0.0 * ureg("W/m2"))
                        * space_b.get("floor_area", 0.0 * ureg("m2"))
                        for interior_lighting_b in space_b["interior_lighting"]
                        if (
                            interior_lighting_b.get("purpose_type")
                            == LIGHTING_PURPOSE.RETAIL_DISPLAY
                        )
                    ]
                )

                proposed_interior_display_w = sum(
                    [
                        interior_lighting_p.get("power_per_area", 0.0 * ureg("W/m2"))
                        * space_p.get("floor_area", 0.0 * ureg("m2"))
                        for interior_lighting_p in space_p["interior_lighting"]
                        if (
                            interior_lighting_p.get("purpose_type")
                            == LIGHTING_PURPOSE.RETAIL_DISPLAY
                        )
                    ]
                )

                return {
                    "maximum_retail_display_w": CalcQ(
                        "electric_power", maximum_retail_display_w
                    ),
                    "minimum_retail_display_w": CalcQ(
                        "electric_power", minimum_retail_display_w
                    ),
                    "baseline_interior_display_w": CalcQ(
                        "electric_power", baseline_interior_display_w
                    ),
                    "proposed_interior_display_w": CalcQ(
                        "electric_power", proposed_interior_display_w
                    ),
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                maximum_retail_display_w = calc_vals["maximum_retail_display_w"]
                minimum_retail_display_w = calc_vals["minimum_retail_display_w"]
                baseline_interior_display_w = calc_vals["baseline_interior_display_w"]
                proposed_interior_display_w = calc_vals["proposed_interior_display_w"]

                return (
                    (proposed_interior_display_w > minimum_retail_display_w)
                    or (
                        not std_equal(
                            baseline_interior_display_w, proposed_interior_display_w
                        )
                    )
                ) and (
                    baseline_interior_display_w
                    < min(proposed_interior_display_w, maximum_retail_display_w)
                )

            def rule_check(self, context, calc_vals=None, data=None):
                minimum_retail_display_w = calc_vals["minimum_retail_display_w"]
                baseline_interior_display_w = calc_vals["baseline_interior_display_w"]
                proposed_interior_display_w = calc_vals["proposed_interior_display_w"]

                return (
                    proposed_interior_display_w < minimum_retail_display_w
                    or self.precision_comparison["minimum_retail_display_w"](
                        minimum_retail_display_w, proposed_interior_display_w
                    )
                ) and self.precision_comparison["baseline_interior_display_w"](
                    proposed_interior_display_w, baseline_interior_display_w
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                minimum_retail_display_w = calc_vals["minimum_retail_display_w"]
                baseline_interior_display_w = calc_vals["baseline_interior_display_w"]
                proposed_interior_display_w = calc_vals["proposed_interior_display_w"]

                return (
                    proposed_interior_display_w < minimum_retail_display_w
                ) and std_equal(
                    baseline_interior_display_w, proposed_interior_display_w
                )
