from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_area_type_window_wall_area_dict import (
    get_area_type_window_wall_area_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

MSG_WARN_MATCHED = "Building is not all new and baseline WWR matches values prescribed in Table G3.1.1-1. However, the fenestration area prescribed in Table G3.1.1-1 does not apply to the existing envelope per TABLE G3.1 baseline column #5 (c). For existing Envelope, the baseline fenestration area must equal the existing fenestration area prior to the proposed work. A manual check is required to verify compliance."
MSG_WARN_MISMATCHED = "Building is not all new and baseline WWR does not match values prescribed in TABLE G3.1.1-1. However, the fenestration area prescribed in TABLE G3.1.1-1 does not apply to the existing envelope per TABLE G3.1 baseline column #5(c). For existing envelope, the baseline fenestration area must equal the existing fenestration area prior to the proposed work. A manual check is required to verify compliance."
WWR_THRESHOLD = 0.4
OTHER = SchemaEnums.schema_enums[
    "VerticalFenestrationBuildingAreaOptions2019ASHRAE901"
].OTHER


class PRM9012019Rule04o58(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule04o58, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule04o58.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-15",
            description="For building areas not shown in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in the proposed design or 40% of gross above-grade wall area, whichever is smaller.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_b["ruleset_model_descriptions"][0].get("constructions")
        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
        }

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule04o58.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={
                    "$": ["building_segments"],
                    "building_segment": [
                        "is_all_new",
                        "area_type_vertical_fenestration",
                    ],
                },
                precision={
                    "wwr_b": {
                        "precision": 0.01,
                        "unit": "",
                    }
                },
            )

        def is_applicable(self, context, data=None):
            building_b = context.BASELINE_0
            area_type_window_wall_area_dict_b = get_area_type_window_wall_area_dict(
                data["climate_zone"], data["constructions"], building_b
            )
            return OTHER in area_type_window_wall_area_dict_b

        def get_calc_vals(self, context, data=None):
            building_b = context.BASELINE_0
            building_p = context.PROPOSED

            area_type_window_wall_area_dict_b = get_area_type_window_wall_area_dict(
                data["climate_zone"], data["constructions"], building_b
            )
            area_type_window_wall_area_dict_p = get_area_type_window_wall_area_dict(
                data["climate_zone"], data["constructions"], building_p
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
            for building_segment in find_all("$.building_segments[*]", building_b):
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
                if self.precision_comparison["wwr_b"](
                    calc_vals["wwr_b"].magnitude,
                    min(calc_vals["wwr_p"].magnitude, WWR_THRESHOLD),
                ):
                    manual_check_msg = MSG_WARN_MATCHED
                else:
                    manual_check_msg = MSG_WARN_MISMATCHED
            return manual_check_msg

        def rule_check(self, context, calc_vals=None, data=None):
            return self.precision_comparison["wwr_b"](
                calc_vals["wwr_b"].magnitude,
                min(calc_vals["wwr_p"].magnitude, WWR_THRESHOLD),
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            return std_equal(
                calc_vals["wwr_b"].magnitude,
                min(calc_vals["wwr_p"].magnitude, WWR_THRESHOLD),
            )
