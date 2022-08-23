from rct229.data.schema_enums import schema_enums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

FLUID_LOOP = schema_enums["FluidLoopOptions"]


def is_hvac_sys_preheat_fluid_loop_attached_to_boiler(rmi_b, hvac_b_id):
    """Returns True if the fluid loop associated with preheat system associated with the HVAC system is attached to a boiler.
        Returns False if this is not the case.

        Parameters
        ----------
        rmi_b : json
            RMD at RuleSetModelInstance level
        hvac_b_id : str
            The HVAC system ID.

        Returns
        -------
        bool
            True: preheat system is attached to a boiler
            False
        """
    is_hvac_sys_preheat_fluid_loop_attached_to_boiler_flag = False
    boilers = find_all("$.ruleset_model_instances[*].boilers[*]", rmi_b)
    loop_boiler_dict = dict()
    for boiler_b in boilers:
        loop_boiler_dict[getattr_(boiler_b, "boiler", "loop")].append(boiler_b)

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value("$.buildings[*].building_segments["
                                               "*].heating_ventilation_air_conditioning_systems",
                                               "id", hvac_b_id,
                                               rmi_b)
    if hvac_b:
        hot_water_loop = find_exactly_one_with_field_value("$.preheat_system[0].hot_water_loop",
                                                           "type", FLUID_LOOP.HEATING, hvac_b)
        if hot_water_loop:
            fluid_loop_b = hot_water_loop["id"]
            if fluid_loop_b in loop_boiler_dict.keys():
                is_hvac_sys_preheat_fluid_loop_attached_to_boiler_flag = True

    return is_hvac_sys_preheat_fluid_loop_attached_to_boiler_flag
