from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

EXTERNAL_FLUID_SOURCE = schema_enums["ExternalFluidSourceOptions"]


def check_purchased_chw_hhw(rmi_b):
    """
    Check if RMD is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source.
    If any system in RMD uses purchased chilled water, function shall return True for purchased chilled water as space cooling source.
    Similarly, if any system in RMD uses purchased hot water or steam, function shall return True for purchased hot water/steam as space heating source.

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
            purchased_chw_loop_array.append(cooling_loop["id"])

            for building_segment in find_all("$..building_segments[*]", rmi_b):
                for hvac_sys in building_segment[
                    "heating_ventilation_air_conditioning_systems"
                ]:
                    if (
                        hvac_sys["cooling_system"]["chilled_water_loop"]
                        in purchased_chw_loop_array
                    ):
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
                    if (
                        hvac_sys["heating_system"]["hot_water_loop"]
                        in purchased_hhw_loop_array
                    ):
                        purchased_chw_hhw_status_dict["purchased_heating"] = True
                        break
                    if hvac_sys.get(
                        "preheat_system"
                    ):  # Prevent an error when preheat system doesn't exist
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
