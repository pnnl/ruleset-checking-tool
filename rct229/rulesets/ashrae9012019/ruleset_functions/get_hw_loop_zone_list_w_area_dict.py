from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_fluid_loop import (
    is_hvac_sys_heating_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_fluid_loop import (
    is_hvac_sys_preheating_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, pint_sum

HEATING_SOURCE = schema_enums["HeatingSourceOptions"]


def get_hw_loop_zone_list_w_area(rmi_b):
    """
    Get the list of zones and their total floor area served by each HHW loop in a baseline ruleset model instance.

    Parameters
    ----------
    rmi_b: The baseline ruleset model instance that needs to get the list of zones with their total floor area served by each HHW loop.

    Returns hw_loop_zone_list_w_area_dictionary A dictionary that saves the list of zones and the total floor area
    served by each HHW loop, i.e. {loop_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "TOTAL_AREA": 10000},
    loop_2.id: {"ZONE_LIST": [zone_10.id], "TOTAL_AREA": 500}}

    -------
    """
    hw_loop_zone_list_w_area_dict = dict()
    for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmi_b):
        zone_area = pint_sum(
            [
                space.get("floor_area", ZERO.AREA)
                for space in find_all("$.spaces[*]", zone)
            ],
            ZERO.AREA,
        )
        for terminal in find_all("$.terminals[*]", zone):
            hhw_loop_id = None
            if terminal.get("heating_source") == HEATING_SOURCE.HOT_WATER:
                # if terminal has reheat.
                # If a terminal heating source is hot water, then it must have a heating_from_loop
                # Otherwise, raise exception
                hhw_loop_id = getattr_(terminal, "terminal", "heating_from_loop")
            elif terminal.get("served_by_heating_ventilating_air_conditioning_system"):
                hvac_id = terminal[
                    "served_by_heating_ventilating_air_conditioning_system"
                ]
                if is_hvac_sys_preheating_type_fluid_loop(rmi_b, hvac_id):
                    # check the case the terminal is connected with an HVAC, whose preheating system is supplied
                    # by a hot water loop. The is_hvac_sys_preheating_type_fluid_loop returns true only
                    # 1. preheat_system exist and,
                    # 2. preheat_system.hot_water_loop exist and,
                    # 3. preheat_system.heating_system_type is HEATING_SYSTEM.FLUID_LOOP
                    hhw_loop_id = find_exactly_one_hvac_system(rmi_b, hvac_id)[
                        "preheat_system"
                    ]["hot_water_loop"]
                elif is_hvac_sys_heating_type_fluid_loop(rmi_b, hvac_id):
                    # check the case the terminal is connected with an HVAC, whose heating system is supplied by
                    # a hot water loop. The is_hvac_sys_heating_type_fluid_loop returns true only
                    # 1. heating_system exist and,
                    # 2. heating_system.hot_water_loop exist and,
                    # 3. heating_system.heating_system_type is HEATING_SYSTEM.FLUID_LOOP
                    hhw_loop_id = find_exactly_one_hvac_system(rmi_b, hvac_id)[
                        "heating_system"
                    ]["hot_water_loop"]
            if type(hhw_loop_id) is str:
                if hhw_loop_id not in hw_loop_zone_list_w_area_dict.keys():
                    hw_loop_zone_list_w_area_dict[hhw_loop_id] = {
                        "zone_list": [],
                        "total_area": ZERO.AREA,
                    }
                # prevent double counting
                if (
                    zone["id"]
                    not in hw_loop_zone_list_w_area_dict[hhw_loop_id]["zone_list"]
                ):
                    hw_loop_zone_list_w_area_dict[hhw_loop_id]["zone_list"].append(
                        zone["id"]
                    )
                    hw_loop_zone_list_w_area_dict[hhw_loop_id][
                        "total_area"
                    ] += zone_area
    return hw_loop_zone_list_w_area_dict
