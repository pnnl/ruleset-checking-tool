from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.schema_enums import SchemaEnums
from rct229.rulesets.ashrae9012019.data_fns.table_G3_111_fns import (
    table_G3_1_1_1_lookup,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_area_type_window_wall_area_dict import (
    NONE_AREA_TYPE,
    get_area_type_window_wall_area_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

CASE3_WARN_MESSAGE = "Building is not all new and baseline WWR matches values prescribed in Table G3.1.1-1. However, the fenestration area prescribed in Table G3.1.1-1 does not apply to the existing envelope per Table G3.1 baseline column #5 (c). For existing envelope, the baseline fenestration area must equal the existing fenestration area prior to the proposed work. A manual check is therefore required to verify compliance."
CASE4_WARN_MESSAGE = "Building is not all new and baseline WWR does not match values prescribed in Table G3.1.1-1. However, the fenestration area prescribed in Table G3.1.1-1 does not apply to the existing envelope per Table G3.1 baseline column #5 (c). For existing envelope, the baseline fenestration area must equal the existing fenestration area prior to the proposed work. A manual check is therefore required to verify compliance"
NONE_WARN_MESSAGE = (
    "Building vertical fenestration area type is missing, manual check is required."
)

OTHER = SchemaEnums.schema_enums["VerticalFenestrationBuildingAreaOptions2019ASHRAE901"].OTHER


class Section5Rule18(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule18, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule18.BuildingRule(),
            index_rmr="baseline",
            id="5-18",
            description="For building area types included in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in Table G3.1.1-1 based on the area of gross above-grade walls that separate conditioned spaces and semi-heated spaces from the exterior.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule18.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["building_segments"],
                    "building_segments[*]": [
                        "is_all_new",
                        "area_type_vertical_fenestration",
                    ],
                },
                index_rmr="baseline",
                each_rule=Section5Rule18.BuildingRule.AreaTypeRule(),
            )

        def create_data(self, context, data=None):
            building = context.baseline
            area_type_window_wall_area_dict_b = get_area_type_window_wall_area_dict(
                data["climate_zone"], building
            )
            is_area_type_all_new_dict = {}
            for building_segment in find_all("$.building_segments[*]", building):
                area_type = building_segment["area_type_vertical_fenestration"]
                # add key-value pair or override the existing value
                is_area_type_all_new_dict[area_type] = building_segment["is_all_new"]

            return {
                "is_area_type_all_new_dict": is_area_type_all_new_dict,
                "area_type_window_wall_ratio_dict": area_type_window_wall_area_dict_b,
            }

        def create_context_list(self, context, data=None):
            # EXAMPLE of reorganizing the context.
            building = context.baseline
            area_type_to_building_segment_dict = {}
            # dict map area_type with list of building_segment
            for building_segment in find_all("$.building_segments[*]", building):
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
                if area_type != OTHER
            ]

        class AreaTypeRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule18.BuildingRule.AreaTypeRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def get_calc_vals(self, context, data=None):
                building_segments_b = context.baseline["building_segments"]
                is_area_type_all_new_dict = data["is_area_type_all_new_dict"]
                area_type_window_wall_ratio_b = data["area_type_window_wall_ratio_dict"]

                # all building segments in AreaType rule has the same area type
                # (see create_context_list function in the parent class)
                area_type = building_segments_b[0]["area_type_vertical_fenestration"]
                area_type_target_wwr = 0.0
                area_type_wwr = (
                    area_type_window_wall_ratio_b[area_type]["total_window_area"]
                    / area_type_window_wall_ratio_b[area_type]["total_wall_area"]
                )
                if area_type != NONE_AREA_TYPE:
                    area_type_target_wwr = table_G3_1_1_1_lookup(area_type)

                return {
                    "area_type": area_type,
                    "is_all_new": is_area_type_all_new_dict[area_type],
                    "area_type_wwr": area_type_wwr,
                    "area_type_target_wwr": area_type_target_wwr["wwr"],
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                # Raise warning...based on checks?
                return (
                    not calc_vals["is_all_new"]
                    or calc_vals["area_type"] == NONE_AREA_TYPE
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                manual_check_msg = ""
                if not calc_vals["is_all_new"]:
                    if std_equal(
                        calc_vals["area_type_wwr"], calc_vals["area_type_target_wwr"]
                    ):
                        manual_check_msg = CASE3_WARN_MESSAGE
                    else:
                        manual_check_msg = CASE4_WARN_MESSAGE
                if calc_vals["area_type"] == "NONE":
                    manual_check_msg = NONE_WARN_MESSAGE
                return manual_check_msg

            def rule_check(self, context, calc_vals=None, data=None):
                area_type_wwr = calc_vals["area_type_wwr"]
                area_type_target_wwr = calc_vals["area_type_target_wwr"]
                return std_equal(area_type_target_wwr, area_type_wwr)
