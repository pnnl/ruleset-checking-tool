from rct229.data_fns.table_G3_111_fns import table_G3_1_1_1_lookup
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_area_type_window_wall_area_dict import (
    get_area_type_window_wall_area_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

MSG_WARN_MATCHED = "Building is not all new and baseline WWR matches values prescribed in Table G3.1.1-1. However, the fenestration area prescribed in Table G3.1.1-1 does not apply to the existing envelope per TABLE G3.1 baseline column #5 (c). For existing Envelope, the baseline fenestration area must equal the existing fenestration area prior to the proposed work. A manual check is required to verify compliance."
MSG_WARN_MISMATCHED = "Building is not all new and baseline WWR does not match values prescribed in TABLE G3.1.1-1. However, the fenestration area prescribed in TABLE G3.1.1-1 does not apply to the existing envelope per TABLE G3.1 baseline column #5(c). For existing envelope, the baseline fenestration area must equal the existing fenestration area prior to the proposed work. A manual check is required to verify compliance."
WWR_THRESHOLD = 0.4


class Section5Rule19(RuleDefinitionListIndexedBase):
    """Rule 19 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule19, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule19.BuildingRule(),
            index_rmr="baseline",
            id="5-19",
            description="For building areas not shown in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in the proposed design or 40% of gross above-grade wall area, whichever is smaller.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule19.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$": ["building_segments"],
                    # "building_segments": [
                    #     "is_all_new",
                    #     "area_type_vertical_fenestration",
                    # ],
                },
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            building_p = context.proposed

            area_type_window_wall_area_dict_b = get_area_type_window_wall_area_dict(
                data["climate_zone"], building_b
            )
            area_type_window_wall_area_dict_p = get_area_type_window_wall_area_dict(
                data["climate_zone"], building_p
            )
            is_area_type_all_new_dict_baseline = {}
            for building_segment in find_all("$..building_segments[*]", building_b):
                area_type = building_segment["area_type_vertical_fenestration"]
                is_area_type_all_new_dict_baseline[area_type] = building_segment[
                    "is_all_new"
                ]
            is_area_type_all_new_dict_proposed = {}
            for building_segment in find_all("$..building_segments[*]", building_p):
                area_type = building_segment["area_type_vertical_fenestration"]
                is_area_type_all_new_dict_proposed[area_type] = building_segment[
                    "is_all_new"
                ]

            return {
                **data,
                "is_area_type_all_new_dict_baseline": is_area_type_all_new_dict_baseline,
                "is_area_type_all_new_dict_proposed": is_area_type_all_new_dict_proposed,
                "area_type_window_wall_ratio_dict_baseline": area_type_window_wall_area_dict_b,
                "area_type_window_wall_ratio_dict_proposed": area_type_window_wall_area_dict_p,
            }


        # def get_calc_vals(self, context, data=None):
        #     # get Baseline window wall areas
        #     building_segments_b = context.baseline["building_segments"]
        #     is_area_type_all_new_dict_b = data["is_area_type_all_new_dict_baseline"]
        #     area_type_window_wall_ratio_b = data[
        #         "area_type_window_wall_ratio_dict_baseline"
        #     ]
        #
        #     area_type_window_wall_ratio_p = data[
        #         "area_type_window_wall_ratio_dict_proposed"
        #     ]
        #
        #     area_type = building_segments_b[0]["area_type_vertical_fenestration"]
        #     area_type_wwr_baseline = 0.0
        #     area_type_wwr_propose = 0.0
        #     area_type_target_wwr = table_G3_1_1_1_lookup(area_type)
        #     if area_type_target_wwr is not "NONE":
        #         area_type_wwr_baseline = (
        #             area_type_window_wall_ratio_b[area_type]["total_window_area"]
        #             / area_type_window_wall_ratio_b[area_type]["total_wall_area"]
        #         )
        #         area_type_wwr_propose = (
        #             area_type_window_wall_ratio_p[area_type]["total_window_area"]
        #             / area_type_window_wall_ratio_p[area_type]["total_wall_area"]
        #         )
        #
        #     return {
        #         "is_all_new_baseline": is_area_type_all_new_dict_b[area_type],
        #         "area_type_wwr_baseline": area_type_wwr_baseline,
        #         "area_type_wwr_propose": area_type_wwr_propose,
        #     }
        #
        # def manual_check_required(self, context, calc_vals=None, data=None):
        #     # Raise warning...based on checks?
        #     return not calc_vals["is_all_new_baseline"]
        #
        # def rule_check(self, context, calc_vals=None, data=None):
        #     area_type_wwr = calc_vals["area_type_wwr_baseline"]
        #     area_type_target_wwr = min(
        #         calc_vals["area_type_wwr_propose"], WWR_THRESHOLD
        #     )
        #     return std_equal(area_type_target_wwr, area_type_wwr)
