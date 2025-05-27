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
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
]
REQUIRED_LOW_DESIGN_WETBULB_TEMP = ureg("55 degF")
REQUIRED_HIGH_DESIGN_WETBULB_TEMP = ureg("90 degF")


class PRM9012019Rule81f32(RuleDefinitionListIndexedBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule81f32, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule81f32.HeatRejectionRule(),
            index_rmd=BASELINE_0,
            id="22-16",
            description="The baseline condenser water design supply temperature shall be calculated using the cooling tower approach to the 0.4% evaporation design wet-bulb temperature, valid for evaporation design wet-bulb temperatures from 55°F to 90°F.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.11 Heat Rejection (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="heat_rejections[*]",
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
            REQUIRED_LOW_DESIGN_WETBULB_TEMP.to(ureg.kelvin)
            <= heat_rejection_wetbulb_temp_b.to(ureg.kelvin)
            <= REQUIRED_HIGH_DESIGN_WETBULB_TEMP.to(ureg.kelvin)
            for heat_rejection_wetbulb_temp_b in find_all(
                "heat_rejections[*].design_wetbulb_temperature", rmd_b
            )
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        heat_rejection_loop_dict = {
            heat_rejection_loop: find_exactly_one_with_field_value(
                "$.fluid_loops[*]", "id", heat_rejection_loop, rmd_b
            )
            for heat_rejection_loop in find_all("$.heat_rejections[*].loop", rmd_b)
        }
        return {"heat_rejection_loop_dict": heat_rejection_loop_dict}

    class HeatRejectionRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule81f32.HeatRejectionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                precision={
                    "design_supply_temperature_b": {
                        "precision": 1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            heat_rejection_b = context.BASELINE_0
            loop_b = heat_rejection_b["loop"]
            design_wetbulb_temperature_b = heat_rejection_b[
                "design_wetbulb_temperature"
            ]
            approach_b = heat_rejection_b["approach"]
            design_supply_temperature_b = getattr_(
                data["heat_rejection_loop_dict"][loop_b],
                "design_supply_temperature",
                "cooling_or_condensing_design_and_control",
                "design_supply_temperature",
            )
            return {
                "loop_b": loop_b,
                "design_wetbulb_temperature_b": CalcQ(
                    "temperature", design_wetbulb_temperature_b
                ),
                "approach_b": CalcQ("temperature", approach_b),
                "design_supply_temperature_b": CalcQ(
                    "temperature", design_supply_temperature_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_wetbulb_temperature = calc_vals["design_wetbulb_temperature_b"]
            approach_b = calc_vals["approach_b"]
            design_supply_temperature_b = calc_vals["design_supply_temperature_b"]

            return self.precision_comparison["design_supply_temperature_b"](
                design_supply_temperature_b.to(ureg.kelvin),
                design_wetbulb_temperature.to(ureg.kelvin) + approach_b.to(ureg.kelvin),
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            design_wetbulb_temperature = calc_vals["design_wetbulb_temperature_b"]
            approach_b = calc_vals["approach_b"]
            design_supply_temperature_b = calc_vals["design_supply_temperature_b"]

            return std_equal(
                design_supply_temperature_b.to(ureg.kelvin),
                design_wetbulb_temperature.to(ureg.kelvin) + approach_b.to(ureg.kelvin),
            )
