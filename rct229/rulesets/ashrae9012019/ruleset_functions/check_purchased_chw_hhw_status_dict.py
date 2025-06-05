from typing import TypedDict

from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.utility_functions import find_exactly_one_fluid_loop

EXTERNAL_FLUID_SOURCE = SchemaEnums.schema_enums["ExternalFluidSourceOptions"]


class PurchasedSystemStatus(TypedDict):
    purchased_cooling: bool
    purchased_heating: bool


def check_purchased_chw_hhw_status_dict(rmd_b: dict) -> PurchasedSystemStatus:
    """
    Check if RMD is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source.
    If any system in RMD uses purchased chilled water, function shall return True for purchased chilled water as space cooling source.
    Similarly, if any system in RMD uses purchased hot water or steam, function shall return True for purchased hot water/steam as space heating source.

    Parameters
    ----------
    rmd_b: json
        RMD at RuleSetModelDescription level

    Returns
    -------
    purchased_chw_hhw_status_dictionary: A dictionary that saves whether RMD is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source,
    i.e. {"purchased_cooling": True, "purchased_heating": False}.

    """
    purchased_chw_hhw_status_dict: PurchasedSystemStatus = {
        "purchased_cooling": False,
        "purchased_heating": False,
    }

    external_fluid_sources = find_all("$.external_fluid_sources[*]", rmd_b)
    if not external_fluid_sources:
        return purchased_chw_hhw_status_dict

    hvac_systems = find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmd_b,
    )
    terminals = find_all(
        "$.buildings[*].building_segments[*].zones[*].terminals[*]", rmd_b
    )
    for external_fluid_source in external_fluid_sources:
        if (
            getattr_(external_fluid_source, "external_fluid_sources", "type")
            == EXTERNAL_FLUID_SOURCE.CHILLED_WATER
        ):
            cooling_loop = find_exactly_one_fluid_loop(
                rmd_b, external_fluid_source["loop"]
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
                rmd_b, external_fluid_source["loop"]
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
