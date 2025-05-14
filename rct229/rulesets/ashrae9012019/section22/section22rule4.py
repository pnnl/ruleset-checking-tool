from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_12B,
]
NOT_APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_1A,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_11_1C,
]
REQUIRED_OUTDOOR_HIGH_LOOP_SUPPLY_TEMP_RESET = ureg("80 degF")
REQUIRED_OUTDOOR_LOW_LOOP_SUPPLY_TEMP_RESET = ureg("60 degF")
REQUIRED_LOOP_SUPPLY_TEMP_OUTDOOR_HIGH = ureg("44 degF")
REQUIRED_LOOP_SUPPLY_TEMP_OUTDOOR_LOW = ureg("54 degF")


class PRM9012019Rule13x50(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule13x50, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule13x50.ChillerFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="22-4",
            description="Baseline chilled water loops that do not use purchased cooling and do not serve any computer rooms (i.e., do not serve baseline system type 11) shall have the chilled water supply temperature reset using the following schedule: 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        ) and any(
            [
                available_type not in NOT_APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        chiller_loop_ids_list = find_all("$.chillers[*].cooling_loop", rmd_b)
        return {"chiller_loop_ids_list": chiller_loop_ids_list}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        loop_chiller_list = data["chiller_loop_ids_list"]
        return fluid_loop_b["id"] in loop_chiller_list

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule13x50.ChillerFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "outdoor_high_for_loop_supply_reset_temperature",
                        "outdoor_low_for_loop_supply_reset_temperature",
                        "loop_supply_temperature_at_outdoor_high",
                        "loop_supply_temperature_at_outdoor_low",
                    ],
                },
                precision={
                    "outdoor_high_for_loop_supply_reset_temperature": {
                        "precision": 1,
                        "unit": "K",
                    },
                    "outdoor_low_for_loop_supply_reset_temperature": {
                        "precision": 1,
                        "unit": "K",
                    },
                    "loop_supply_temperature_at_outdoor_high": {
                        "precision": 1,
                        "unit": "K",
                    },
                    "loop_supply_temperature_at_outdoor_low": {
                        "precision": 1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            outdoor_high_for_loop_supply_reset_temperature = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["outdoor_high_for_loop_supply_reset_temperature"]
            outdoor_low_for_loop_supply_reset_temperature = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["outdoor_low_for_loop_supply_reset_temperature"]
            loop_supply_temperature_at_outdoor_high = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["loop_supply_temperature_at_outdoor_high"]
            loop_supply_temperature_at_outdoor_low = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["loop_supply_temperature_at_outdoor_low"]

            return {
                "outdoor_high_for_loop_supply_reset_temperature": CalcQ(
                    "temperature", outdoor_high_for_loop_supply_reset_temperature
                ),
                "required_outdoor_high_for_loop_supply_reset_temperature": CalcQ(
                    "temperature", REQUIRED_OUTDOOR_HIGH_LOOP_SUPPLY_TEMP_RESET
                ),
                "outdoor_low_for_loop_supply_reset_temperature": CalcQ(
                    "temperature", outdoor_low_for_loop_supply_reset_temperature
                ),
                "required_outdoor_low_for_loop_supply_reset_temperature": CalcQ(
                    "temperature", REQUIRED_OUTDOOR_LOW_LOOP_SUPPLY_TEMP_RESET
                ),
                "loop_supply_temperature_at_outdoor_high": CalcQ(
                    "temperature", loop_supply_temperature_at_outdoor_high
                ),
                "required_loop_supply_temperature_at_outdoor_high": CalcQ(
                    "temperature", REQUIRED_LOOP_SUPPLY_TEMP_OUTDOOR_HIGH
                ),
                "loop_supply_temperature_at_outdoor_low": CalcQ(
                    "temperature", loop_supply_temperature_at_outdoor_low
                ),
                "required_loop_supply_temperature_at_outdoor_low": CalcQ(
                    "temperature", REQUIRED_LOOP_SUPPLY_TEMP_OUTDOOR_LOW
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            outdoor_high_for_loop_supply_reset_temperature = calc_vals[
                "outdoor_high_for_loop_supply_reset_temperature"
            ]
            required_outdoor_high_for_loop_supply_reset_temperature = calc_vals[
                "required_outdoor_high_for_loop_supply_reset_temperature"
            ]
            outdoor_low_for_loop_supply_reset_temperature = calc_vals[
                "outdoor_low_for_loop_supply_reset_temperature"
            ]
            required_outdoor_low_for_loop_supply_reset_temperature = calc_vals[
                "required_outdoor_low_for_loop_supply_reset_temperature"
            ]
            loop_supply_temperature_at_outdoor_high = calc_vals[
                "loop_supply_temperature_at_outdoor_high"
            ]
            required_loop_supply_temperature_at_outdoor_high = calc_vals[
                "required_loop_supply_temperature_at_outdoor_high"
            ]
            loop_supply_temperature_at_outdoor_low = calc_vals[
                "loop_supply_temperature_at_outdoor_low"
            ]
            required_loop_supply_temperature_at_outdoor_low = calc_vals[
                "required_loop_supply_temperature_at_outdoor_low"
            ]

            return (
                self.precision_comparison[
                    "outdoor_high_for_loop_supply_reset_temperature"
                ](
                    outdoor_high_for_loop_supply_reset_temperature.to(ureg.kelvin),
                    required_outdoor_high_for_loop_supply_reset_temperature.to(
                        ureg.kelvin
                    ),
                )
                and self.precision_comparison[
                    "outdoor_low_for_loop_supply_reset_temperature"
                ](
                    outdoor_low_for_loop_supply_reset_temperature.to(ureg.kelvin),
                    required_outdoor_low_for_loop_supply_reset_temperature.to(
                        ureg.kelvin
                    ),
                )
                and self.precision_comparison[
                    "loop_supply_temperature_at_outdoor_high"
                ](
                    loop_supply_temperature_at_outdoor_high.to(ureg.kelvin),
                    required_loop_supply_temperature_at_outdoor_high.to(ureg.kelvin),
                )
                and self.precision_comparison["loop_supply_temperature_at_outdoor_low"](
                    loop_supply_temperature_at_outdoor_low.to(ureg.kelvin),
                    required_loop_supply_temperature_at_outdoor_low.to(ureg.kelvin),
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            outdoor_high_for_loop_supply_reset_temperature = calc_vals[
                "outdoor_high_for_loop_supply_reset_temperature"
            ]
            required_outdoor_high_for_loop_supply_reset_temperature = calc_vals[
                "required_outdoor_high_for_loop_supply_reset_temperature"
            ]
            outdoor_low_for_loop_supply_reset_temperature = calc_vals[
                "outdoor_low_for_loop_supply_reset_temperature"
            ]
            required_outdoor_low_for_loop_supply_reset_temperature = calc_vals[
                "required_outdoor_low_for_loop_supply_reset_temperature"
            ]
            loop_supply_temperature_at_outdoor_high = calc_vals[
                "loop_supply_temperature_at_outdoor_high"
            ]
            required_loop_supply_temperature_at_outdoor_high = calc_vals[
                "required_loop_supply_temperature_at_outdoor_high"
            ]
            loop_supply_temperature_at_outdoor_low = calc_vals[
                "loop_supply_temperature_at_outdoor_low"
            ]
            required_loop_supply_temperature_at_outdoor_low = calc_vals[
                "required_loop_supply_temperature_at_outdoor_low"
            ]

            return (
                std_equal(
                    outdoor_high_for_loop_supply_reset_temperature.to(ureg.kelvin),
                    required_outdoor_high_for_loop_supply_reset_temperature.to(
                        ureg.kelvin
                    ),
                )
                and std_equal(
                    outdoor_low_for_loop_supply_reset_temperature.to(ureg.kelvin),
                    required_outdoor_low_for_loop_supply_reset_temperature.to(
                        ureg.kelvin
                    ),
                )
                and std_equal(
                    loop_supply_temperature_at_outdoor_high.to(ureg.kelvin),
                    required_loop_supply_temperature_at_outdoor_high.to(ureg.kelvin),
                )
                and std_equal(
                    loop_supply_temperature_at_outdoor_low.to(ureg.kelvin),
                    required_loop_supply_temperature_at_outdoor_low.to(ureg.kelvin),
                )
            )
