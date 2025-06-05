from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hw_loop_zone_list_w_area_dict import (
    get_hw_loop_zone_list_w_area,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

DESIGN_TEMP_RESET_TYPE = SchemaEnums.schema_enums["TemperatureResetOptions"]
DESIGN_SUPPLY_TEMP_AT_OUTDOOR_HIGH = 150 * ureg("degF")
DESIGN_SUPPLY_TEMP_AT_OUTDOOR_LOW = 180 * ureg("degF")
DESIGN_OUTDOOR_TEMP_FOR_RESET_HIGH = 50 * ureg("degF")
DESIGN_OUTDOOR_TEMP_FOR_RESET_LOW = 20 * ureg("degF")


class PRM9012019Rule58s22(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule58s22, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule58s22.HeatingFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="21-8",
            description="When the baseline building requires boilers, (for baseline system type = 1,5,7,11 and 12), HWST for the baseline building shall be reset using an outdoor air dry-bulb reset schedule. 180F at 20F OAT, 150Fat 50F OAT, ramped linearly between 150F and 180F.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.3.3 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        hw_loop_zone_list_w_area_dict_b = get_hw_loop_zone_list_w_area(rmd_b)
        boiler_loop_ids_b = find_all("$.boilers[*].loop", rmd_b)
        boiler_fluid_loops_set_b = set(
            boiler_loop_id
            for boiler_loop_id in boiler_loop_ids_b
            if boiler_loop_id in hw_loop_zone_list_w_area_dict_b
        )
        return len(boiler_fluid_loops_set_b) > 0

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        hw_loop_zone_list_w_area_dict_b = get_hw_loop_zone_list_w_area(rmd_b)
        boiler_loop_ids_b = find_all("$.boilers[*].loop", rmd_b)
        boiler_fluid_loops_set_b = set(
            boiler_loop_id
            for boiler_loop_id in boiler_loop_ids_b
            if boiler_loop_id in hw_loop_zone_list_w_area_dict_b
        )
        return {"boiler_loop_ids_list_b": list(boiler_fluid_loops_set_b)}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        boiler_loop_ids_b = data["boiler_loop_ids_list_b"]
        return fluid_loop_b["id"] in boiler_loop_ids_b

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule58s22.HeatingFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["heating_design_and_control"],
                    "heating_design_and_control": [
                        "temperature_reset_type",
                        "outdoor_high_for_loop_supply_reset_temperature",
                        "outdoor_low_for_loop_supply_reset_temperature",
                        "loop_supply_temperature_at_outdoor_high",
                        "loop_supply_temperature_at_outdoor_low",
                    ],
                },
                precision={
                    "design_outdoor_high_for_loop_supply_reset_temperature_b": {
                        "precision": 1,
                        "unit": "K",
                    },
                    "design_outdoor_low_for_loop_supply_reset_temperature_b": {
                        "precision": 1,
                        "unit": "K",
                    },
                    "design_supply_temperature_at_outdoor_high_b": {
                        "precision": 1,
                        "unit": "K",
                    },
                    "design_supply_temperature_at_outdoor_low_b": {
                        "precision": 1,
                        "unit": "K",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            temperature_reset_type_b = fluid_loop_b["heating_design_and_control"][
                "temperature_reset_type"
            ]
            design_outdoor_high_for_loop_supply_reset_temperature_b = fluid_loop_b[
                "heating_design_and_control"
            ]["outdoor_high_for_loop_supply_reset_temperature"]
            design_outdoor_low_for_loop_supply_reset_temperature_b = fluid_loop_b[
                "heating_design_and_control"
            ]["outdoor_low_for_loop_supply_reset_temperature"]
            design_supply_temperature_at_outdoor_high_b = fluid_loop_b[
                "heating_design_and_control"
            ]["loop_supply_temperature_at_outdoor_high"]
            design_supply_temperature_at_outdoor_low_b = fluid_loop_b[
                "heating_design_and_control"
            ]["loop_supply_temperature_at_outdoor_low"]
            return {
                "temperature_reset_type_b": temperature_reset_type_b,
                "design_outdoor_high_for_loop_supply_reset_temperature_b": CalcQ(
                    "temperature",
                    design_outdoor_high_for_loop_supply_reset_temperature_b,
                ),
                "design_outdoor_low_for_loop_supply_reset_temperature_b": CalcQ(
                    "temperature",
                    design_outdoor_low_for_loop_supply_reset_temperature_b,
                ),
                "design_supply_temperature_at_outdoor_high_b": CalcQ(
                    "temperature", design_supply_temperature_at_outdoor_high_b
                ),
                "design_supply_temperature_at_outdoor_low_b": CalcQ(
                    "temperature", design_supply_temperature_at_outdoor_low_b
                ),
                "required_outdoor_high_for_loop_supply_reset_temperature_b": CalcQ(
                    "temperature", DESIGN_OUTDOOR_TEMP_FOR_RESET_HIGH
                ),
                "required_outdoor_low_for_loop_supply_reset_temperature_b": CalcQ(
                    "temperature", DESIGN_OUTDOOR_TEMP_FOR_RESET_LOW
                ),
                "required_supply_temperature_at_outdoor_high_b": CalcQ(
                    "temperature", DESIGN_SUPPLY_TEMP_AT_OUTDOOR_HIGH
                ),
                "required_supply_temperature_at_outdoor_low_b": CalcQ(
                    "temperature", DESIGN_SUPPLY_TEMP_AT_OUTDOOR_LOW
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_reset_type_b = calc_vals["temperature_reset_type_b"]
            design_outdoor_high_for_loop_supply_reset_temperature_b = calc_vals[
                "design_outdoor_high_for_loop_supply_reset_temperature_b"
            ]
            design_outdoor_low_for_loop_supply_reset_temperature_b = calc_vals[
                "design_outdoor_low_for_loop_supply_reset_temperature_b"
            ]
            design_supply_temperature_at_outdoor_high_b = calc_vals[
                "design_supply_temperature_at_outdoor_high_b"
            ]
            design_supply_temperature_at_outdoor_low_b = calc_vals[
                "design_supply_temperature_at_outdoor_low_b"
            ]
            required_outdoor_high_for_loop_supply_reset_temperature_b = calc_vals[
                "required_outdoor_high_for_loop_supply_reset_temperature_b"
            ]
            required_outdoor_low_for_loop_supply_reset_temperature_b = calc_vals[
                "required_outdoor_low_for_loop_supply_reset_temperature_b"
            ]
            required_supply_temperature_at_outdoor_high_b = calc_vals[
                "required_supply_temperature_at_outdoor_high_b"
            ]
            required_supply_temperature_at_outdoor_low_b = calc_vals[
                "required_supply_temperature_at_outdoor_low_b"
            ]
            return (
                temperature_reset_type_b == DESIGN_TEMP_RESET_TYPE.OUTSIDE_AIR_RESET
                and self.precision_comparison[
                    "design_outdoor_high_for_loop_supply_reset_temperature_b"
                ](
                    design_outdoor_high_for_loop_supply_reset_temperature_b.to(
                        ureg.kelvin
                    ),
                    required_outdoor_high_for_loop_supply_reset_temperature_b.to(
                        ureg.kelvin
                    ),
                )
                and self.precision_comparison[
                    "design_outdoor_low_for_loop_supply_reset_temperature_b"
                ](
                    design_outdoor_low_for_loop_supply_reset_temperature_b.to(
                        ureg.kelvin
                    ),
                    required_outdoor_low_for_loop_supply_reset_temperature_b.to(
                        ureg.kelvin
                    ),
                )
                and self.precision_comparison[
                    "design_supply_temperature_at_outdoor_high_b"
                ](
                    design_supply_temperature_at_outdoor_high_b.to(ureg.kelvin),
                    required_supply_temperature_at_outdoor_high_b.to(ureg.kelvin),
                )
                and self.precision_comparison[
                    "design_supply_temperature_at_outdoor_low_b"
                ](
                    design_supply_temperature_at_outdoor_low_b.to(ureg.kelvin),
                    required_supply_temperature_at_outdoor_low_b.to(ureg.kelvin),
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            temperature_reset_type_b = calc_vals["temperature_reset_type_b"]
            design_outdoor_high_for_loop_supply_reset_temperature_b = calc_vals[
                "design_outdoor_high_for_loop_supply_reset_temperature_b"
            ]
            design_outdoor_low_for_loop_supply_reset_temperature_b = calc_vals[
                "design_outdoor_low_for_loop_supply_reset_temperature_b"
            ]
            design_supply_temperature_at_outdoor_high_b = calc_vals[
                "design_supply_temperature_at_outdoor_high_b"
            ]
            design_supply_temperature_at_outdoor_low_b = calc_vals[
                "design_supply_temperature_at_outdoor_low_b"
            ]
            required_outdoor_high_for_loop_supply_reset_temperature_b = calc_vals[
                "required_outdoor_high_for_loop_supply_reset_temperature_b"
            ]
            required_outdoor_low_for_loop_supply_reset_temperature_b = calc_vals[
                "required_outdoor_low_for_loop_supply_reset_temperature_b"
            ]
            required_supply_temperature_at_outdoor_high_b = calc_vals[
                "required_supply_temperature_at_outdoor_high_b"
            ]
            required_supply_temperature_at_outdoor_low_b = calc_vals[
                "required_supply_temperature_at_outdoor_low_b"
            ]
            return (
                temperature_reset_type_b == DESIGN_TEMP_RESET_TYPE.OUTSIDE_AIR_RESET
                and std_equal(
                    design_outdoor_high_for_loop_supply_reset_temperature_b.to(
                        ureg.kelvin
                    ),
                    required_outdoor_high_for_loop_supply_reset_temperature_b.to(
                        ureg.kelvin
                    ),
                )
                and std_equal(
                    design_outdoor_low_for_loop_supply_reset_temperature_b.to(
                        ureg.kelvin
                    ),
                    required_outdoor_low_for_loop_supply_reset_temperature_b.to(
                        ureg.kelvin
                    ),
                )
                and std_equal(
                    design_supply_temperature_at_outdoor_high_b.to(ureg.kelvin),
                    required_supply_temperature_at_outdoor_high_b.to(ureg.kelvin),
                )
                and std_equal(
                    design_supply_temperature_at_outdoor_low_b.to(ureg.kelvin),
                    required_supply_temperature_at_outdoor_low_b.to(ureg.kelvin),
                )
            )
