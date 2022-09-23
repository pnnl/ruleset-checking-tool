from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-12",
    "SYS-13",
    "SYS-7B",
    "SYS-8B",
    "SYS-12B",
    "SYS-13B",
]
NOT_APPLICABLE_SYS_TYPES = [
    "SYS-11.1",
    "SYS-11.2",
    "SYS-11.1A",
    "SYS-11.2A",
    "SYS-11B",
    "SYS-11C",
]
REQUIRED_OUTDOOR_HIGH_LOOP_SUPPLY_TEMP_RESET = 80 * ureg("degF")
REQUIRED_OUTDOOR_LOW_LOOP_SUPPLY_TEMP_RESET = 60 * ureg("degF")
REQUIRED_LOOP_SUPPLY_TEMP_OUTDOOR_HIGH = 44 * ureg("degF")
REQUIRED_LOOP_SUPPLY_TEMP_OUTDOOR_LOW = 54 * ureg("degF")


class Section22Rule4(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule4, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule4.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-4",
            description="For Baseline chilled water loop that is not purchased chilled water and does not serve any computer room HVAC systems, chilled-water supply temperature shall be reset using the following schedule: 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F.",
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11-a": ["hvac_sys_11_a"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        ) and not any(
            [key in NOT_APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        chiller_loop_ids = find_all("chillers[*].cooling_loop", rmi_b)
        return {"loop_chiller_dict": chiller_loop_ids}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        loop_chiller_dict = data["loop_chiller_dict"]
        return fluid_loop_b["id"] in loop_chiller_dict

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule4.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "outdoor_high_for_loop_supply_temperature_reset",
                        "outdoor_low_for_loop_supply_temperature_reset",
                        "loop_supply_temperature_at_outdoor_high",
                        "loop_supply_temperature_at_outdoor_low",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            outdoor_high_for_loop_supply_temperature_reset = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["outdoor_high_for_loop_supply_temperature_reset"]
            outdoor_low_for_loop_supply_temperature_reset = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["outdoor_low_for_loop_supply_temperature_reset"]
            loop_supply_temperature_at_outdoor_high = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["loop_supply_temperature_at_outdoor_high"]
            loop_supply_temperature_at_outdoor_low = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["loop_supply_temperature_at_outdoor_low"]

            return {
                "outdoor_high_for_loop_supply_temperature_reset": CalcQ(
                    "temperature", outdoor_high_for_loop_supply_temperature_reset
                ),
                "outdoor_low_for_loop_supply_temperature_reset": CalcQ(
                    "temperature", outdoor_low_for_loop_supply_temperature_reset
                ),
                "loop_supply_temperature_at_outdoor_high": CalcQ(
                    "temperature", loop_supply_temperature_at_outdoor_high
                ),
                "loop_supply_temperature_at_outdoor_low": CalcQ(
                    "temperature", loop_supply_temperature_at_outdoor_low
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            outdoor_high_for_loop_supply_temperature_reset = calc_vals[
                "outdoor_high_for_loop_supply_temperature_reset"
            ]
            outdoor_low_for_loop_supply_temperature_reset = calc_vals[
                "outdoor_low_for_loop_supply_temperature_reset"
            ]
            loop_supply_temperature_at_outdoor_high = calc_vals[
                "loop_supply_temperature_at_outdoor_high"
            ]
            loop_supply_temperature_at_outdoor_low = calc_vals[
                "loop_supply_temperature_at_outdoor_low"
            ]

            return (
                std_equal(
                    outdoor_high_for_loop_supply_temperature_reset.to(ureg.kelvin),
                    REQUIRED_OUTDOOR_HIGH_LOOP_SUPPLY_TEMP_RESET.to(ureg.kelvin),
                )
                and std_equal(
                    outdoor_low_for_loop_supply_temperature_reset.to(ureg.kelvin),
                    REQUIRED_OUTDOOR_LOW_LOOP_SUPPLY_TEMP_RESET.to(ureg.kelvin),
                )
                and std_equal(
                    loop_supply_temperature_at_outdoor_high.to(ureg.kelvin),
                    REQUIRED_LOOP_SUPPLY_TEMP_OUTDOOR_HIGH.to(ureg.kelvin),
                )
                and std_equal(
                    loop_supply_temperature_at_outdoor_low.to(ureg.kelvin),
                    REQUIRED_LOOP_SUPPLY_TEMP_OUTDOOR_LOW.to(ureg.kelvin),
                )
            )
