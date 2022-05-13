from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
    get_surface_conditioning_category_dict,
)
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
    get_zone_conditioning_category_dict,
)

from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ONE, ZERO
from rct229.utils.std_comparisons import std_equal


class Section5Rule49(RuleDefinitionListIndexedBase):
    """Rule 49 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule49, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule49.BuildingRule(),
            index_rmr="proposed",
            id="5-49",
            description="The proposed air leakage rate of the building envelope (I75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 0.6 cfm/ft2 for buildings providing verification in accordance with Section 5.9.1.2. The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4. Exceptions: When whole-building air leakage testing, in accordance with Section 5.4.3.1.1, is specified during design and completed after construction, the proposed design air leakage rate of the building envelope shall be as measured..",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):  # put it under the "BuildingRule"
        rmr_proposed = context.proposed
        return {"climate_zone": rmr_proposed["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule49.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                each_rule=Section5Rule49.BuildingRule.ZoneRule(),
                index_rmr="proposed",
                list_path="$..zones[*]",
            )

        def create_data(self, context, data=None):
            building_p = context.proposed

            return {
                **data,
                "scc_dict_p": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_p
                ),
                "zcc_dict_p": get_zone_conditioning_category_dict(
                    data["climate_zone"], building_p
                ),
            }

        class ZoneRule(RuleDefinitionBase):  # change to the zoneRule
            def __init__(self):
                super(Section5Rule49.BuildingRule.ZoneRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, False, True),
                    required_fields={
                        "$": ["infiltration", "surfaces"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                zone_p = context.proposed

                scc_dict_p = data["scc_dict_p"]
                zcc_dict_p = data["zcc_dict_p"]

                building_total_envelope_area = 0.0
                building_total_air_leakage_rate = 0.0
                building_total_measured_air_leakage_rate = 0.0
                empty_measured_air_leakage_rate_flow_flag = False

                building_total_envelope_area = sum(
                    [
                        surface.get("area")
                        for surface in find_all("surfaces[*]", zone_p)
                        if scc_dict_p[surface["id"]] != SCC.UNREGULATED
                    ],
                    ZERO.AREA,
                )

                if zone_p["infiltration"].get("measured_air_leakage_rate"):
                    building_total_measured_air_leakage_rate += zone_p["infiltration"][
                        "measured_air_leakage_rate"
                    ]
                else:
                    empty_measured_air_leakage_rate_flow_flag = True
                    if zcc_dict_p[zone_p["id"]] in [
                        ZCC.CONDITIONED_RESIDENTIAL,
                        ZCC.CONDITIONED_NON_RESIDENTIAL,
                        ZCC.SEMI_HEATED,
                    ]:
                        building_total_air_leakage_rate += zone_p["infiltration"][
                            "infiltration_flow_rate"
                        ]

                target_air_leakage_rate_75pa_p = (
                    0.6 * ONE.FLOW / ONE.AREA
                ) * building_total_envelope_area

                return {
                    "building_total_air_leakage_rate": building_total_air_leakage_rate,
                    "building_total_measured_air_leakage_rate": building_total_measured_air_leakage_rate,
                    "target_air_leakage_rate_75pa_p": target_air_leakage_rate_75pa_p,
                    "empty_measured_air_leakage_rate_flow_flag": empty_measured_air_leakage_rate_flow_flag,
                }

            def rule_check(self, context, calc_vals, data=None):
                building_total_air_leakage_rate = calc_vals[
                    "building_total_air_leakage_rate"
                ]
                building_total_measured_air_leakage_rate = calc_vals[
                    "building_total_measured_air_leakage_rate"
                ]
                target_air_leakage_rate_75pa_p = calc_vals[
                    "target_air_leakage_rate_75pa_p"
                ]
                empty_measured_air_leakage_rate_flow_flag = calc_vals[
                    "empty_measured_air_leakage_rate_flow_flag"
                ]

                return std_equal(
                    building_total_air_leakage_rate,
                    0.112 * target_air_leakage_rate_75pa_p,
                ) or (
                    building_total_air_leakage_rate
                    != 0.112 * target_air_leakage_rate_75pa_p
                    and empty_measured_air_leakage_rate_flow_flag == False
                    and std_equal(
                        building_total_air_leakage_rate,
                        0.112 * building_total_measured_air_leakage_rate,
                    )
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                return "The building total air leakage rate is not equal to the required proposed design air leakage rate at 75Pa with a Conversion Factor of 0.112 as per section G3.1.1.4. and Measured air leakage rate is not entered for all conditioned and semi-heated zones. Verify the proposed air leakage rate is modeled correctly."
