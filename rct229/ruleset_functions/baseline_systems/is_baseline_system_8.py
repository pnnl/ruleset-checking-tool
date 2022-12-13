from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fan_configs_parallel import (
    are_all_terminal_fan_configs_parallel,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_electric import (
    are_all_terminal_heat_sources_electric,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.do_all_terminals_have_one_fan import (
    do_all_terminals_have_one_fan,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_fluid_loop import (
    is_hvac_sys_cooling_type_fluid_loop,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_chiller import (
    is_hvac_sys_fluid_loop_attached_to_chiller,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_CHW import (
    is_hvac_sys_fluid_loop_purchased_chw,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_purchased_heating import (
    is_hvac_sys_preheat_fluid_loop_purchased_heating,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_elec_resistance import (
    is_hvac_sys_preheating_type_elec_resistance,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_fluid_loop import (
    is_hvac_sys_preheating_type_fluid_loop,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    find_exactly_one_hvac_system,
)

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_baseline_system_8(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 8 (VAV with Parallel Fan-Powered Boxes and Reheat), system 8a (system 8 with purchased CHW), system 8b (system 8 with purchased heating), or 8c (system 8 with purchased heating and purchased chilled water).

    Parameters
    ----------
    rmi_b json
         To evaluate if the hvac system is modeled as either Sys-11.1, Sys-11.1a, Sys-11b, Sys-11c, or Not_Sys_11.1 in the B_RMI.
     hvac_b_id list
         The id of the hvac system to evaluate.
     terminal_unit_id_list
         List list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
     zone_id_list list
         list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

    Returns
    -------
    The function returns either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 8 (VAV with Parallel Fan-Powered Boxes and Reheat ), system 8a (system 8 with purchased CHW), system 8b (system 8 with purchased heating), or 8c (system 8 with purchased heating and purchased chilled water).
    """

    is_baseline_system_8 = HVAC_SYS.UNMATCHED

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)

    # check if the hvac system has the required sub systems for system type 11.1
    has_required_heating_sys = (
        hvac_b.get("heating_system") is None
        or hvac_b["heating_system"].get("heating_system_type") is None
        or hvac_b["heating_system"]["heating_system_type"] == HEATING_SYSTEM.NONE
    )

    has_required_preheat_sys = hvac_b.get("preheat_system") is not None

    are_sys_data_matched = (
        # short-circuit the logic if no required data is found.
        has_required_heating_sys
        and has_required_preheat_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_cooling_type_fluid_loop(rmi_b, hvac_b_id)
        and is_hvac_sys_fan_sys_vsd(rmi_b, hvac_b_id)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and do_all_terminals_have_one_fan(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_VAV(rmi_b, terminal_unit_id_list)
        and are_all_terminal_fan_configs_parallel(rmi_b, terminal_unit_id_list)
    )

    if are_sys_data_matched:
        if is_hvac_sys_preheating_type_elec_resistance(
            rmi_b, hvac_b_id
        ) and are_all_terminal_heat_sources_electric(rmi_b, terminal_unit_id_list):
            if is_hvac_sys_fluid_loop_attached_to_chiller(rmi_b, hvac_b_id):
                is_baseline_system_8 = HVAC_SYS.SYS_8
            elif is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id):
                is_baseline_system_8 = HVAC_SYS.SYS_8A
        elif is_hvac_sys_preheating_type_fluid_loop(rmi_b, hvac_b_id):
            if (
                is_hvac_sys_preheat_fluid_loop_purchased_heating(rmi_b, hvac_b_id)
                and are_all_terminal_heat_sources_hot_water(
                    rmi_b, terminal_unit_id_list
                )
                and are_all_terminal_heating_loops_purchased_heating(
                    rmi_b, terminal_unit_id_list
                )
            ):
                if is_hvac_sys_fluid_loop_attached_to_chiller(rmi_b, hvac_b_id):
                    is_baseline_system_8 = HVAC_SYS.SYS_8B
                elif is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id):
                    is_baseline_system_8 = HVAC_SYS.SYS_8C

    return is_baseline_system_8


SYS_8_TEST_RMD = {
    "id": "ASHRAE229 1",
    "ruleset_model_instances": [
        {
            "id": "RMD 1",
            "buildings": [
                {
                    "id": "Building 1",
                    "building_open_schedule": "Required Building Schedule 1",
                    "building_segments": [
                        {
                            "id": "Building Segment 1",
                            "zones": [
                                {
                                    "id": "Thermal Zone 8",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8",
                                            "heating_source": "ELECTRIC",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "fan": {"id": "fan 8"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8a",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8a",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8a",
                                            "heating_source": "ELECTRIC",
                                            "heating_from_loop": "Boiler Loop 1",
                                            "fan": {"id": "fan 8a"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8b",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8b",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8b",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan": {"id": "fan 8b"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                                {
                                    "id": "Thermal Zone 8c",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "VAV Air Terminal 8c",
                                            "is_supply_ducted": True,
                                            "type": "VARIABLE_AIR_VOLUME",
                                            "served_by_heating_ventilating_air_conditioning_system": "System 8c",
                                            "heating_source": "HOT_WATER",
                                            "heating_from_loop": "Purchased HW Loop 1",
                                            "fan": {"id": "fan 8c"},
                                            "fan_configuration": "PARALLEL",
                                        }
                                    ],
                                },
                            ],
                            "heating_ventilating_air_conditioning_systems": [
                                {
                                    "id": "System 8",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 1",
                                        "heating_system_type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 8a",
                                    "cooling_system": {
                                        "id": "CHW Coil 8a",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased Chilled Water Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8a",
                                        "heating_system_type": "ELECTRIC_RESISTANCE",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8a",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 8a"}],
                                        "return_fans": [{"id": "Return Fan 8a"}],
                                    },
                                },
                                {
                                    "id": "System 8b",
                                    "cooling_system": {
                                        "id": "CHW Coil 8b",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Secondary CHW Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8b",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8b",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                                {
                                    "id": "System 8c",
                                    "cooling_system": {
                                        "id": "CHW Coil 8C",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Purchased Chilled Water Loop 1",
                                    },
                                    "preheat_system": {
                                        "id": "Preheat Coil 8C",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Purchased HW Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "VAV Fan System 8C",
                                        "fan_control": "VARIABLE_SPEED_DRIVE",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                },
                            ],
                        }
                    ],
                }
            ],
            "boilers": [
                {
                    "id": "Boiler 1",
                    "loop": "Boiler Loop 1",
                    "energy_source_type": "NATURAL_GAS",
                }
            ],
            "external_fluid_source": [
                {
                    "id": "Purchased CW 1",
                    "loop": "Purchased Chilled Water Loop 1",
                    "type": "CHILLED_WATER",
                },
                {
                    "id": "Purchased HW 1",
                    "loop": "Purchased HW Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased CW 2",
                    "loop": "Chilled Water Loop 2",
                    "type": "CHILLED_WATER",
                },
            ],
            "chillers": [{"id": "Chiller 1", "cooling_loop": "Chiller Loop 1"}],
            "pumps": [
                {
                    "id": "Boiler Pump 1",
                    "loop_or_piping": "Boiler Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "Chiller Pump 1",
                    "loop_or_piping": "Chiller Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "Secondary CHW Pump",
                    "loop_or_piping": "Secondary CHW Loop 1",
                    "speed_control": "VARIABLE_SPEED",
                },
            ],
            "fluid_loops": [
                {"id": "Boiler Loop 1", "type": "HEATING"},
                {"id": "Purchased HW Loop 1", "type": "HEATING"},
                {
                    "id": "Chiller Loop 1",
                    "type": "COOLING",
                    "child_loops": [{"id": "Secondary CHW Loop 1", "type": "COOLING"}],
                },
                {"id": "Purchased Chilled Water Loop 1", "type": "COOLING"},
            ],
        }
    ],
}


a = is_baseline_system_8(
    SYS_8_TEST_RMD["ruleset_model_instances"][0],
    "System 8c",
    ["VAV Air Terminal 8c"],
    ["Thermal Zone 8c"],
)
print(a)
