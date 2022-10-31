from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

EXTERNAL_FLUID_SOURCE = schema_enums["ExternalFluidSourceOptions"]

rmi = {
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
                                    "id": "Thermal Zone 1",
                                    "thermostat_cooling_setpoint_schedule": "Required Cooling Schedule 1",
                                    "thermostat_heating_setpoint_schedule": "Required Heating Schedule 1",
                                    "terminals": [
                                        {
                                            "id": "CAV Air Terminal 1",
                                            "is_supply_ducted": True,
                                            "type": "CONSTANT_AIR_VOLUME",
                                            "served_by_heating_ventilation_air_conditioning_system": "System 12",
                                        }
                                    ],
                                }
                            ],
                            "heating_ventilation_air_conditioning_systems": [
                                {
                                    "id": "System 12",
                                    "cooling_system": {
                                        "id": "CHW Coil 1",
                                        "cooling_system_type": "FLUID_LOOP",
                                        "chilled_water_loop": "Chilled Water Loop 1",
                                    },
                                    "heating_system": {
                                        "id": "Boiler Coil 1",
                                        "heating_system_type": "FLUID_LOOP",
                                        "hot_water_loop": "Boiler Loop 1",
                                    },
                                    "fan_system": {
                                        "id": "CAV Fan System 1",
                                        "fan_control": "CONSTANT",
                                        "supply_fans": [{"id": "Supply Fan 1"}],
                                        "return_fans": [{"id": "Return Fan 1"}],
                                    },
                                }
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
                    "loop": "Chilled Water Loop 1",
                    "type": "CHILLED_WATER",
                },
                {
                    "id": "Purchased CW 2",
                    "loop": "Chilled Water Loop 2",
                    "type": "CHILLED_WATER",
                },
                {
                    "id": "Purchased HW 1",
                    "loop": "Hot Water Loop 1",
                    "type": "HOT_WATER",
                },
                {
                    "id": "Purchased Steam 1",
                    "loop": "Steam Loop 1",
                    "type": "STEAM",
                },
            ],
            "pumps": [
                {
                    "id": "Boiler Pump 1",
                    "loop_or_piping": "Boiler Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
                {
                    "id": "CHW Pump 1",
                    "loop_or_piping": "Chilled Water Loop 1",
                    "speed_control": "FIXED_SPEED",
                },
            ],
            "fluid_loops": [
                {
                    "id": "Boiler Loop 1",
                    "type": "HEATING",
                },
                {
                    "id": "Chilled Water Loop 1",
                    "type": "COOLING",
                    "child_loops": [
                        {"id": "CHW1 Child Loop 1"},
                        {"id": "CHW1 Child Loop 2"},
                    ],
                },
                {
                    "id": "Chilled Water Loop 2",
                    "type": "COOLING",
                    "child_loops": [
                        {"id": "CHW2 Child Loop 1"},
                        {"id": "CHW2 Child Loop 2"},
                    ],
                },
                {
                    "id": "Hot Water Loop 1",
                    "type": "HEATING",
                    "child_loops": [
                        {"id": "HW1 Child Loop 1"},
                        {"id": "HW1 Child Loop 2"},
                    ],
                },
                {
                    "id": "Steam Loop 1",
                    "type": "HEATING",
                    "child_loops": [
                        {"id": "HW2 Child Loop 1"},
                        {"id": "HW2 Child Loop 2"},
                    ],
                },
            ],
        }
    ],
}


def check_purchased_chw_hhw(rmi_b):
    """
    Check if RMD is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source. If any system in RMD uses purchased chilled water, function shall return True for purchased chilled water as space cooling source. Similarly, if any system in RMD uses purchased hot water or steam, function shall return True for purchased hot water/steam as space heating source.

    Parameters
    ----------
    rmi_b:

    Returns
    -------

    """
    purchased_chw_hhw_status_dict = {
        "purchased_cooling": False,
        "purchased_heating": False,
    }

    if not find_all("$..external_fluid_source[*]", rmi_b):
        return purchased_chw_hhw_status_dict

    for external_fluid_source in find_all("$..external_fluid_source[*]", rmi_b):
        if external_fluid_source["type"] == EXTERNAL_FLUID_SOURCE.CHILLED_WATER:
            cooling_loop = find_exactly_one_with_field_value(
                "$..fluid_loops[*]", "id", external_fluid_source["loop"], rmi_b
            )
            purchased_chw_loop_array = [
                loop["id"] for loop in cooling_loop["child_loops"]
            ]
            purchased_chw_loop_array.append(external_fluid_source["id"])

            for building_segment in find_all("$..building_segments[*]", rmi_b):
                for hvac_sys in building_segment[
                    "heating_ventilation_air_conditioning_systems"
                ]:
                    for cooling_system in hvac_sys["cooling_system"]:
                        if cooling_system in purchased_chw_loop_array:
                            purchased_chw_hhw_status_dict["purchased_cooling"] = True
                            break

        else:  # HOT_WATER or STEAM type
            heating_loop = find_exactly_one_with_field_value(
                "$..fluid_loops[*]", "id", external_fluid_source["loop"], rmi_b
            )

            purchased_hhw_loop_array = [
                loop["id"] for loop in heating_loop["child_loops"]
            ]
            purchased_hhw_loop_array.append(heating_loop["id"])

            for building_segment in find_all("$..building_segments[*]", rmi_b):
                for hvac_sys in building_segment[
                    "heating_ventilation_air_conditioning_systems"
                ]:

                    # for heating_system in hvac_sys["heating_system"]:
                    #     print(hvac_sys)
                    #     print(hvac_sys["heating_system"])
                    #     print(hvac_sys["heating_system"]["hot_water_loop"])

                    if (
                        hvac_sys["heating_system"]["hot_water_loop"]
                        in purchased_hhw_loop_array
                    ):
                        purchased_chw_hhw_status_dict["purchased_heating"] = True
                        break
                    if find_all(
                        "$..preheat_system[*]", rmi_b
                    ):  ## TODO needs to be checked
                        for preheat_system in hvac_sys["preheat_system"]:
                            if (
                                preheat_system["hot_water_loop"]
                                in purchased_hhw_loop_array
                            ):
                                purchased_chw_hhw_status_dict[
                                    "purchased_heating"
                                ] = True
                                break

                for zone in building_segment["zones"]:
                    for terminal in zone["terminals"]:
                        if (
                            terminal.get("heating_from_loop")
                            in purchased_hhw_loop_array
                        ):
                            purchased_chw_hhw_status_dict["purchased_heating"] = True
                            break
                        if (
                            terminal.get("cooling_from_loop")
                            in purchased_chw_loop_array
                        ):
                            purchased_chw_hhw_status_dict["purchased_cooling"] = True
                            break

    return purchased_chw_hhw_status_dict


testing = check_purchased_chw_hhw(rmi)
print(f"testing:\n{testing}")
