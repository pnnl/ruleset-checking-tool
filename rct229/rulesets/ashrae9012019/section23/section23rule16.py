from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal
from rct229.utils.utility_functions import find_exactly_one_fluid_loop

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
]

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]
FLUID_LOOP = SchemaEnums.schema_enums["FluidLoopOptions"]
REQUIRED_SET_POINT_REDUCTION = 20.0 * ureg("delta_degF")


class PRM9012019Rule79i34(RuleDefinitionListIndexedBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule79i34, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule79i34.HVACRule(),
            index_rmd=BASELINE_0,
            id="23-16",
            description="Systems 5 - 8, the baseline system shall be modeled with preheat coils controlled to a fixed set point 20F less than the design room heating temperature setpoint.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Section G3.1.3.19 Preheat Coils (Systems 5 through 8)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        return any(
            [
                baseline_system_types_dict[system_type]
                and baseline_system_type_compare(
                    system_type, applicable_sys_type, False
                )
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        # set hvac_id with highest zone_design_heating_setpoint
        hvac_max_zone_setpoint_dict = {}
        for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmd_b):
            # handle indirectly conditioned zones, which do not have terminals.
            zone_design_heating_setpoint = zone.get(
                "design_thermostat_heating_setpoint", ZERO.TEMPERATURE
            )
            hvac_max_zone_setpoint_dict.update(
                {
                    hvac_id: max(
                        zone_design_heating_setpoint,
                        hvac_max_zone_setpoint_dict.get(hvac_id, ZERO.TEMPERATURE),
                    )
                    for hvac_id in find_all(
                        "$.terminals[*].served_by_heating_ventilating_air_conditioning_system",
                        zone,
                    )
                }
            )

        # find preheat_system's hot water loop type
        hot_water_loop_type_dict = {
            preheat_system["hot_water_loop"]: find_exactly_one_fluid_loop(
                rmd_b, preheat_system["hot_water_loop"]
            )["type"]
            for preheat_system in find_all(
                "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].preheat_system",
                rmd_b,
            )
        }

        # find applicable hvac sys ids
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        return {
            "hvac_max_zone_setpoint_dict": hvac_max_zone_setpoint_dict,
            "hot_water_loop_type_dict": hot_water_loop_type_dict,
            "applicable_hvac_sys_ids": applicable_hvac_sys_ids,
        }

    def list_filter(self, context_item, data):
        hvac_sys_b = context_item.BASELINE_0
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return hvac_sys_b["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule79i34.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["id", "preheat_system"],
                    "preheat_system": [
                        "type",
                        "hot_water_loop",
                        "heating_coil_setpoint",
                    ],
                },
                precision={
                    "heating_coil_setpoint": {
                        "precision": 0.1,
                        "unit": "delta_degC",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            heating_ventilating_air_conditioning_systems_b = context.BASELINE_0

            hvac_id = heating_ventilating_air_conditioning_systems_b["id"]
            preheat_system_b = heating_ventilating_air_conditioning_systems_b[
                "preheat_system"
            ]
            heating_system_type = preheat_system_b["type"]
            hot_water_loop_type = data["hot_water_loop_type_dict"][
                preheat_system_b["hot_water_loop"]
            ]
            heating_coil_setpoint = preheat_system_b["heating_coil_setpoint"]
            hvac_max_zone_setpoint = data["hvac_max_zone_setpoint_dict"][hvac_id]

            return {
                "hvac_id": hvac_id,
                "heating_system_type_b": heating_system_type,
                "hot_water_loop_type": hot_water_loop_type,
                "heating_coil_setpoint": CalcQ("temperature", heating_coil_setpoint),
                "hvac_max_zone_setpoint": CalcQ("temperature", hvac_max_zone_setpoint),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            heating_system_type_b = calc_vals["heating_system_type_b"]
            hot_water_loop_type = calc_vals["hot_water_loop_type"]
            heating_coil_setpoint = calc_vals["heating_coil_setpoint"]
            hvac_max_zone_setpoint = calc_vals["hvac_max_zone_setpoint"]

            return (
                heating_system_type_b == HEATING_SYSTEM.FLUID_LOOP
                and hot_water_loop_type == FLUID_LOOP.HEATING
                and self.precision_comparison["heating_coil_setpoint"](
                    heating_coil_setpoint,
                    hvac_max_zone_setpoint - REQUIRED_SET_POINT_REDUCTION,
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            heating_system_type_b = calc_vals["heating_system_type_b"]
            hot_water_loop_type = calc_vals["hot_water_loop_type"]
            heating_coil_setpoint = calc_vals["heating_coil_setpoint"]
            hvac_max_zone_setpoint = calc_vals["hvac_max_zone_setpoint"]

            return (
                heating_system_type_b == HEATING_SYSTEM.FLUID_LOOP
                and hot_water_loop_type == FLUID_LOOP.HEATING
                and std_equal(
                    heating_coil_setpoint,
                    hvac_max_zone_setpoint - REQUIRED_SET_POINT_REDUCTION,
                )
            )
