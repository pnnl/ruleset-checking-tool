from rct229.data_fns.table_G3_111_fns import table_G3_1_1_1_lookup
from rct229.rule_engine.rule_base import RuleDefinitionListIndexedBase, RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_area_type_window_wall_area_dict import get_area_type_window_wall_area_dict
from rct229.utils.jsonpath_utils import find_all

MSG_WARN_MATCHED = "BUILDING IS NOT ALL NEW AND BASELINE WWR MATCHES VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."
MSG_WARN_MISMATCHED = "BUILDING IS NOT ALL NEW AND BASELINE WWR DOES NOT MATCH VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5(c). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."


class Section5Rule18(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule18, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule18.BuildingRule(),
            index_rmr="baseline",
            id="5-18",
            description="For building area types included in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in Table G3.1.1-1 based on the area of gross above-grade walls that separate conditioned spaces and semi-heated spaces from the exterior.",
            rmr_context="ruleset_model_instances/0/buildings",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule18.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={},
                each_rule=Section5Rule18.BuildingRule.BuildingSegmentRule(),
                index_rmr="baseline",
            )

        def create_context_list(self, context, data=None):
            building = context.baseline
            # List of all baseline roof surfaces to become the context for RoofRule
            return [
                UserBaselineProposedVals(None, building_segment, None)
                for building_segment in find_all("$..building_segments[*]", building)
            ]

        def create_data(self, context, data=None):
            building = context.baseline
            # Merge into the existing data dict
            return {
                **data,
                "area_type_vertical_fenestration": get_area_type_window_wall_area_dict(
                    data["climate_zone"], building
                ),
            }

        class BuildingSegmentRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule18.BuildingRule.BuildingSegmentRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                    required_fields={"$": ["is_all_new"]},
                    )

            def get_calc_vals(self, context, data=None):
                building_segment_b = context.baseline
                window_wall_areas_dictionary_b = data["area_type_vertical_fenestration"]

                area_type_vertical_fenestration = building_segment_b.get("area_type_vertical_fenestration")
                building_segment_wwr = 0.0
                target_area_type_wwr = 0.0

                if area_type_vertical_fenestration is None:
                    # if the building segment has no area_type_vertical_fenestration, then set the building_segment_wwr
                    # to "None" list of window_wall_ratio. - indicate manual check is required
                    building_segment_wwr = window_wall_areas_dictionary_b["None"]["total_window_area"] \
                                             / window_wall_areas_dictionary_b["None"]["total_wall_area"]
                    target_area_type_wwr = None
                elif window_wall_areas_dictionary_b[area_type_vertical_fenestration]["total_wall_area"] == 0:
                    # Calculation error - unlikely to happen, added for code completeness
                    # indicate manual check is required
                    building_segment_wwr = None
                    target_area_type_wwr = None
                else:
                    building_segment_wwr = window_wall_areas_dictionary_b[area_type_vertical_fenestration]["total_window_area"] \
                    / window_wall_areas_dictionary_b[area_type_vertical_fenestration]["total_wall_area"]

                    if table_G3_1_1_1_lookup(building_segment_b.get("area_type_vertical_fenestration")):
                        target_area_type_wwr = table_G3_1_1_1_lookup(building_segment_b.get("area_type_vertical_fenestration"))
                    else:
                        # Building_segment has area_type_vertical_fenestration but not it is not in Table G3.1.1-1.
                        # Set it as Other type, which is 40%
                        target_area_type_wwr = 0.4

                return {
                    "id": building_segment_b["id"],
                    "area_type_vertical_fenestration": area_type_vertical_fenestration,
                    "building_segment_wwr": building_segment_wwr,
                    "target_area_type_wwr": target_area_type_wwr
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                return calc_vals["target_area_type_wwr"] is None

            def rule_check(self, context, calc_vals=None, data=None):
                building_segment = context.baseline
                building_segment_wwr = calc_vals["building_segment_wwr"]
                target_area_type_wwr = calc_vals["target_area_type_wwr"]
                if building_segment["is_all_new"]:
                    return building_segment_wwr == target_area_type_wwr
                else:
                    if building_segment_wwr == target_area_type_wwr:
                        calc_vals["message"] = MSG_WARN_MATCHED
                        return True
                    else:
                        calc_vals["message"] = MSG_WARN_MISMATCHED
                        return False


