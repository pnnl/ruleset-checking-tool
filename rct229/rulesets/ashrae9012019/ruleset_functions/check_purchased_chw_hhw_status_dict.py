from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_fluid_loop,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one

EXTERNAL_FLUID_SOURCE = schema_enums["ExternalFluidSourceOptions"]


def check_purchased_chw_hhw_status_dict(rmi_b):
    """
    Check if RMI is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source.
    If any system in RMI uses purchased chilled water, function shall return True for purchased chilled water as space cooling source.
    Similarly, if any system in RMI uses purchased hot water or steam, function shall return True for purchased hot water/steam as space heating source.

    Parameters
    ----------
    rmi_b: json
        RMI at RuleSetModelInstance level

    Returns
    -------
    purchased_chw_hhw_status_dictionary: A dictionary that saves whether RMI is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source,
    i.e. {"purchased_cooling": True, "purchased_heating": False}.

    """
    purchased_chw_hhw_status_dict = {
        "purchased_cooling": False,
        "purchased_heating": False,
    }

    external_fluid_sources = find_all("$.external_fluid_source[*]", rmi_b)
    if not external_fluid_sources:
        return purchased_chw_hhw_status_dict

    hvac_systems = find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmi_b,
    )
    terminals = find_all(
        "$.buildings[*].building_segments[*].zones[*].terminals[*]", rmi_b
    )
    for external_fluid_source in external_fluid_sources:
        if (
            getattr_(external_fluid_source, "external_fluid_source", "type")
            == EXTERNAL_FLUID_SOURCE.CHILLED_WATER
        ):
            cooling_loop = find_exactly_one_fluid_loop(
                rmi_b, external_fluid_source["loop"]
            )

            purchased_chw_loop_array = find_all("$.child_loops[*].id", cooling_loop) + [
                cooling_loop["id"]
            ]

            for hvac_sys in hvac_systems:
                if (
                    not purchased_chw_hhw_status_dict["purchased_cooling"]
                    and find_one("$.cooling_system.chilled_water_loop", hvac_sys)
                    in purchased_chw_loop_array
                ):
                    purchased_chw_hhw_status_dict["purchased_cooling"] = True

            for terminal in terminals:
                if (
                    not purchased_chw_hhw_status_dict["purchased_cooling"]
                    and terminal.get("cooling_from_loop") in purchased_chw_loop_array
                ):
                    purchased_chw_hhw_status_dict["purchased_cooling"] = True

        else:  # HOT_WATER or STEAM type
            assert external_fluid_source["type"] in [
                EXTERNAL_FLUID_SOURCE.HOT_WATER,
                EXTERNAL_FLUID_SOURCE.STEAM,
            ]  # needs to add more heating types if new types are added in the schema

            heating_loop = find_exactly_one_fluid_loop(
                rmi_b, external_fluid_source["loop"]
            )

            purchased_hhw_loop_array = find_all("$.child_loops[*].id", heating_loop) + [
                heating_loop["id"]
            ]

            for hvac_sys in hvac_systems:
                if not purchased_chw_hhw_status_dict["purchased_heating"]:
                    if (
                        find_one("$.heating_system.hot_water_loop", hvac_sys)
                        in purchased_hhw_loop_array
                    ) or (
                        hvac_sys.get("preheat_system")
                        and hvac_sys["preheat_system"]["hot_water_loop"]
                        in purchased_hhw_loop_array
                    ):
                        purchased_chw_hhw_status_dict["purchased_heating"] = True

            for terminal in terminals:
                if (
                    not purchased_chw_hhw_status_dict["purchased_heating"]
                    and terminal.get("heating_from_loop") in purchased_hhw_loop_array
                ):
                    purchased_chw_hhw_status_dict["purchased_heating"] = True

    return purchased_chw_hhw_status_dict
