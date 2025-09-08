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
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_1B,
]
REQUIRED_LOOP_SUPPLY_TEMP_AT_LOW_LOAD = ureg("54 degF")


class PRM9012019Rule52t53(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule52t53, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule52t53.ChillerFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="22-6",
            description="Baseline chilled water loops that do not use purchased chilled water and do serve computer rooms (i.e., baseline system type 11) shall have a maximum reset chilled water supply temperature setpoint of 54F.",
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
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        chiller_loop_ids_list = find_all("$.chillers[*].cooling_loop", rmd_b)
        return {"chiller_loop_ids_list": chiller_loop_ids_list}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        chiller_loop_ids_list = data["chiller_loop_ids_list"]
        return fluid_loop_b["id"] in chiller_loop_ids_list

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule52t53.ChillerFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "loop_supply_temperature_at_low_load",
                    ],
                },
                precision={
                    "loop_supply_temperature_at_low_load": {
                        "precision": 1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            loop_supply_temperature_at_low_load = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["loop_supply_temperature_at_low_load"]

            return {
                "loop_supply_temperature_at_low_load": CalcQ(
                    "temperature", loop_supply_temperature_at_low_load
                ),
                "required_loop_supply_temperature_at_low_load": CalcQ(
                    "temperature", REQUIRED_LOOP_SUPPLY_TEMP_AT_LOW_LOAD
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            loop_supply_temperature_at_low_load = calc_vals[
                "loop_supply_temperature_at_low_load"
            ]
            required_loop_supply_temperature_at_low_load = calc_vals[
                "required_loop_supply_temperature_at_low_load"
            ]

            return self.precision_comparison["loop_supply_temperature_at_low_load"](
                loop_supply_temperature_at_low_load.to(ureg.kelvin),
                required_loop_supply_temperature_at_low_load.to(ureg.kelvin),
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            loop_supply_temperature_at_low_load = calc_vals[
                "loop_supply_temperature_at_low_load"
            ]
            required_loop_supply_temperature_at_low_load = calc_vals[
                "required_loop_supply_temperature_at_low_load"
            ]

            return std_equal(
                loop_supply_temperature_at_low_load.to(ureg.kelvin),
                required_loop_supply_temperature_at_low_load.to(ureg.kelvin),
            )
