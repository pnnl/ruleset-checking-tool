from rct229.data_fns.table_G3_111_fns import table_G3_1_1_1_lookup
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_area_type_window_wall_area_dict import get_area_type_window_wall_area_dict
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

MSG_WARN_MATCHED = "BUILDING IS NOT ALL NEW AND BASELINE WWR MATCHES VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."
MSG_WARN_MISMATCHED = "BUILDING IS NOT ALL NEW AND BASELINE WWR DOES NOT MATCH VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5(c). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."


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

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule19.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$": ["building_segments"],
                    "building_segment": [
                        "is_all_new",
                        "area_type_vertical_fenestration",
                    ],
                },
                each_rule=Section5Rule19.BuildingRule.BuildingSegmentRule(),
                index_rmr="baseline",
            )

        def create_data(self, context, data=None):
            print(data)
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
                is_area_type_all_new_dict_baseline[area_type] = building_segment["is_all_new"]
            is_area_type_all_new_dict_proposed = {}
            for building_segment in find_all("$..building_segments[*]", building_b):
                area_type = building_segment["area_type_vertical_fenestration"]
                is_area_type_all_new_dict_proposed[area_type] = building_segment["is_all_new"]

            return {
                **data,
                "is_area_type_all_new_dict_baseline": is_area_type_all_new_dict_baseline,
                "is_area_type_all_new_dict_proposed": is_area_type_all_new_dict_proposed,
                "area_type_window_wall_ratio_dict_baseline": area_type_window_wall_area_dict_b,
                "area_type_window_wall_ratio_dict_proposed": area_type_window_wall_area_dict_p,
            }

        def create_context_list(self, context, data=None):
            building = context.baseline
            area_type_to_building_segment_dict = {}
            # dict map area_type with list of building_segment
            for building_segment in find_all("$..building_segments[*]", building):
                area_type = building_segment["area_type_vertical_fenestration"]
                if area_type not in area_type_to_building_segment_dict:
                    area_type_to_building_segment_dict[area_type] = {
                        "id": area_type,
                        "building_segments": [],
                    }
                area_type_to_building_segment_dict[area_type][
                    "building_segments"
                ].append(building_segment)
            # create list based on area_type
            return [
                UserBaselineProposedVals(None, building_segments, None)
                for area_type, building_segments in area_type_to_building_segment_dict.items()
            ]

        class BuildingSegmentRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule19.BuildingRule.BuildingSegmentRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    required_fields={"$": ["is_all_new"]},
                    )

            def get_calc_vals(self, context, data=None):
                print(context)
                # get Baseline window wall areas
                building_segments_b = context.baseline["building_segments"]
                # get propose window wall areas
                building_segments_b = context.proposed["building_segments"]

                # check if the wwr is equal to the proposed design


                return None
                # return {
                #     "is_all_new": is_area_type_all_new_dict[area_type],
                #     "area_type_wwr": area_type_wwr,
                #     "area_type_target_wwr": area_type_target_wwr["wwr"],
                # }

            def manual_check_required(self, context, calc_vals=None, data=None):
                # Raise warning...based on checks?
                return not calc_vals["is_all_new"]

            def rule_check(self, context, calc_vals=None, data=None):
                area_type_wwr = calc_vals["area_type_wwr"]
                area_type_target_wwr = calc_vals["area_type_target_wwr"]
                return std_equal(area_type_target_wwr, area_type_wwr)
