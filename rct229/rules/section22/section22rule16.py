from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import (
    find_all,
    find_exactly_one_with_field_value,
)
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-11.1",
    "SYS-11.2",
    "SYS-12",
    "SYS-13",
    "SYS-7B",
    "SYS-8B",
    "SYS-11B",
    "SYS-12B",
    "SYS-13B",
]
REQUIRED_LOW_DESIGN_WETBULB_TEMP = ureg("55 degF")
REQUIRED_HIGH_DESIGN_WETBULB_TEMP = ureg("90 degF")


class Section22Rule16(RuleDefinitionListIndexedBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule16, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule16.ChillerHeatRejectionRule(),
            index_rmr="baseline",
            id="22-16",
            description="The baseline condenser-water design supply temperature shall be calculated using the cooling tower approach to the 0.4% evaporation design wet-bulb temperature, valid for wet-bulbs from 55°F to 90°F.",
            rmr_context="ruleset_model_instances/0",
            list_path="heat_rejections[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11B": ["hvac_sys_11_b"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES and wet-bulb temp is in the correct range then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        ) and all(
            REQUIRED_LOW_DESIGN_WETBULB_TEMP.to(ureg.kelvin)
            <= heat_rejection_wetbulb_temp_b
            <= REQUIRED_HIGH_DESIGN_WETBULB_TEMP.to(ureg.kelvin)
            for heat_rejection_wetbulb_temp_b in find_all(
                "heat_rejections[*].design_wetbulb_temperature", rmi_b
            )
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        supply_temperature_b_dict = {
            heat_rejection_loop: find_exactly_one_with_field_value(
                "$..fluid_loops[*]", "id", heat_rejection_loop, rmi_b
            )["cooling_or_condensing_design_and_control"]["design_supply_temperature"]
            for heat_rejection_loop in find_all("heat_rejections[*].loop", rmi_b)
        }

        return {"supply_temperature_b_dict": supply_temperature_b_dict}

    class ChillerHeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule16.ChillerHeatRejectionRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["design_wetbulb_temperature", "approach", "loop"],
                },
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.baseline
            wbt_b = heat_rejection_b["design_wetbulb_temperature"]
            approach_b = heat_rejection_b["approach"]
            loop_b = heat_rejection_b["loop"]
            return {
                "wbt_b": CalcQ("temperature", wbt_b),
                "approach_b": CalcQ("temperature", approach_b),
                "loop_b": loop_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            wbt_b = calc_vals["wbt_b"]
            approach_b = calc_vals["approach_b"]
            loop_b = calc_vals["loop_b"]
            supply_temperature_b = data["supply_temperature_b_dict"][loop_b]
            return std_equal(
                supply_temperature_b.to(ureg.kelvin),
                (wbt_b + approach_b).to(ureg.kelvin),
            )
