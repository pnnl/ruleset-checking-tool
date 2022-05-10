from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all


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
                each_rule=Section5Rule49.BuildingRule.BuildingSegmentRule(),
                index_rmr="proposed",
                list_path="$..zones[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            building_p = context.proposed

            return {
                **data,
                "zcc_dict_b": get_zone_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
                "zcc_dict_p": get_zone_conditioning_category_dict(
                    data["climate_zone"], building_p
                ),
            }

        # def list_filter(self, context_item, data=None):
        #     zcc_dict_p = data["zcc_dict_p"]
        #     zone_p = context_item.proposed
        #     return (zcc_dict_p[zone_p["id"]] != SCC.UNREGULATED # SurfaceConditioningCategory -> UNREGULATED
        #             and  [zone_p["id"]] in [ZCC.CONDITIONED_RESIDENTIAL, ZCC.CONDITIONED_NON_RESIDENTIAL, ZCC.SEMI_HEATED]
        #             )
        #
        class BuildingSegmentRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule49.BuildingRule.BuildingSegmentRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, False, True),
                    required_fields={
                        "$": ["infiltration"],
                        "infiltration[*]": ["measured_air_leakage_rate"],
                    },
                )
        #
        #     def get_calc_vals(self, context, data=None):
        #         zone_b = context.baseline
        #         zone_p = context.proposed
        #
        #         building_total_envelope_area  =
        #
        #         building_total_measured_air_leakage_rate = 0
        #
        #         building_total_measured_air_leakage_rate += zone_p["infiltration"]["measured_air_leakage_rate"]
        #
        #         return {
        #             "building_total_envelope_area": building_total_envelope_area,
        #             "building_total_measured_air_leakage_rate ": building_total_measured_air_leakage_rate,
        #         }
        #
        #     def rule_check(self, context, calc_vals, data=None):
        #         return (
        #             calc_vals["target_air_leakage_rate_75pa_p"] == 0.6 * calc_vals["building_total_envelope_area"]
        #         )
