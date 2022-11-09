from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_fluid_loop,
)
from rct229.utils.jsonpath_utils import find_all, find_one

EXTERNAL_FLUID_SOURCE = schema_enums["ExternalFluidSourceOptions"]


def check_purchased_chw_hhw(rmi_b):
    """
    Check if RMD is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source.
    If any system in RMD uses purchased chilled water, function shall return True for purchased chilled water as space cooling source.
    Similarly, if any system in RMD uses purchased hot water or steam, function shall return True for purchased hot water/steam as space heating source.

    Parameters
    ----------
    rmi_b: json
        RMD at RuleSetModelInstance level

    Returns
    -------
    purchased_chw_hhw_status_dictionary: A dictionary that saves whether RMD is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source,
    i.e. {"PURCHASED_COOLING": TRUE, "PURCHASED_HEATING": FALSE}.

    """
    purchased_chw_hhw_status_dict = {
        "purchased_cooling": False,
        "purchased_heating": False,
    }

    if not find_all("$..external_fluid_source[*]", rmi_b):
        return purchased_chw_hhw_status_dict

    for external_fluid_source in find_all("$..external_fluid_source[*]", rmi_b):
        if external_fluid_source["type"] == EXTERNAL_FLUID_SOURCE.CHILLED_WATER:
            cooling_loop = find_exactly_one_fluid_loop(
                rmi_b, external_fluid_source["loop"]
            )
            for loop in find_one("$.child_loops[*]", cooling_loop):
                print(loop)

            purchased_chw_loop_array = [
                find_one("$.child_loops[*]", cooling_loop)["id"]
            ]
            purchased_chw_loop_array.append(find_one("$.id", cooling_loop))

            for hvac_sys in find_all(
                "$..heating_ventilation_air_conditioning_systems[*]", rmi_b
            ):
                if (
                    find_one("$.cooling_system.chilled_water_loop", hvac_sys)
                    in purchased_chw_loop_array
                ):
                    purchased_chw_hhw_status_dict["purchased_cooling"] = True
                    break

        else:  # HOT_WATER or STEAM type
            heating_loop = find_exactly_one_fluid_loop(
                rmi_b, external_fluid_source["loop"]
            )

            purchased_hhw_loop_array = [
                find_one("$.child_loops[*]", heating_loop)["id"]
            ]
            purchased_hhw_loop_array.append(find_one("$.id", heating_loop))

            for hvac_sys in find_all(
                "$..heating_ventilation_air_conditioning_systems[*]", rmi_b
            ):
                if (
                    find_one("$.heating_system.hot_water_loop", hvac_sys)
                    in purchased_hhw_loop_array
                ):
                    purchased_chw_hhw_status_dict["purchased_heating"] = True
                    break
                if hvac_sys.get(
                    "preheat_system"
                ):  # Prevent an error when preheat system doesn't exist
                    for preheat_system in hvac_sys["preheat_system"]:
                        if preheat_system["hot_water_loop"] in purchased_hhw_loop_array:
                            purchased_chw_hhw_status_dict["purchased_heating"] = True
                            break

            for terminal in find_all("$..terminals[*]", rmi_b):
                if terminal.get("heating_from_loop") in purchased_hhw_loop_array:
                    purchased_chw_hhw_status_dict["purchased_heating"] = True
                    break
                if terminal.get("cooling_from_loop") in purchased_chw_loop_array:
                    purchased_chw_hhw_status_dict["purchased_cooling"] = True
                    break

    return purchased_chw_hhw_status_dict
