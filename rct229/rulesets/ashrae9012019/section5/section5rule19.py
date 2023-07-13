from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_area_type_window_wall_area_dict import (
    get_area_type_window_wall_area_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

MSG_WARN_MATCHED = "Building is not all new and baseline WWR matches values prescribed in Table G3.1.1-1. However, the fenestration area prescribed in Table G3.1.1-1 does not apply to the existing envelope per TABLE G3.1 baseline column #5 (c). For existing Envelope, the baseline fenestration area must equal the existing fenestration area prior to the proposed work. A manual check is required to verify compliance."
MSG_WARN_MISMATCHED = "Building is not all new and baseline WWR does not match values prescribed in TABLE G3.1.1-1. However, the fenestration area prescribed in TABLE G3.1.1-1 does not apply to the existing envelope per TABLE G3.1 baseline column #5(c). For existing envelope, the baseline fenestration area must equal the existing fenestration area prior to the proposed work. A manual check is required to verify compliance."
WWR_THRESHOLD = 0.4
OTHER = schema_enums["VerticalFenestrationBuildingAreaOptions2019ASHRAE901"].OTHER


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
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionBase):
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
            )

        def is_applicable(self, context, data=None):
            building_b = context.baseline
            area_type_window_wall_area_dict_b = get_area_type_window_wall_area_dict(
                data["climate_zone"], building_b
            )
            return OTHER in area_type_window_wall_area_dict_b

        def get_calc_vals(self, context, data=None):
            building_b = context.baseline
            building_p = context.proposed

            area_type_window_wall_area_dict_b = get_area_type_window_wall_area_dict(
                data["climate_zone"], building_b
            )
            area_type_window_wall_area_dict_p = get_area_type_window_wall_area_dict(
                data["climate_zone"], building_p
            )

            wwr_b = (
                area_type_window_wall_area_dict_b[OTHER]["total_window_area"]
                / area_type_window_wall_area_dict_b[OTHER]["total_wall_area"]
            )
            wwr_p = (
                area_type_window_wall_area_dict_p[OTHER]["total_window_area"]
                / area_type_window_wall_area_dict_p[OTHER]["total_wall_area"]
            )

            manual_check_flag = False
            for building_segment in find_all("$..building_segments[*]", building_b):
                if building_segment["area_type_vertical_fenestration"] == OTHER:
                    if not building_segment["is_all_new"]:
                        manual_check_flag = True

            return {
                "wwr_b": wwr_b,
                "wwr_p": wwr_p,
                "manual_check_flag": manual_check_flag,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            return calc_vals["manual_check_flag"]

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            manual_check_msg = ""
            if calc_vals["manual_check_flag"]:
                if std_equal(
                    calc_vals["wwr_b"], min(calc_vals["wwr_p"], WWR_THRESHOLD)
                ):
                    manual_check_msg = MSG_WARN_MATCHED
                else:
                    manual_check_msg = MSG_WARN_MISMATCHED
            return manual_check_msg

        def rule_check(self, context, calc_vals=None, data=None):
            return not calc_vals["manual_check_flag"] and std_equal(
                calc_vals["wwr_b"], min(calc_vals["wwr_p"], WWR_THRESHOLD)
            )
