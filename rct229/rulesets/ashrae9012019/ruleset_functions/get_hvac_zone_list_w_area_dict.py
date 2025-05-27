from typing import TypedDict

from pint import Quantity
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all, find_exactly_required_fields
from rct229.utils.pint_utils import ZERO

# Intended for export and internal use
GET_HVAC_ZONE_LIST_W_AREA_DICT__REQUIRED_FIELDS = {
    "building": {
        "building_segments[*].zones[*].spaces[*]": [
            "floor_area",
        ],
    }
}


class HVACZoneListArea(TypedDict):
    total_area: Quantity
    zone_list: list[str]


def get_hvac_zone_list_w_area_by_rmd_dict(rmd: dict) -> dict[str, HVACZoneListArea]:
    """
    RMD version of the get_hvac_zone_list_w_area_dict function

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema

    Returns
    -------
    dict
        A dictionary of the form
        {
            <hvac_system id>: {
                "zone_list": [<zones served by the hvac system>],
                "total_area": <total area served by the hvac system>
            }
        }
    """
    hvac_zone_list_w_area_dict = {}
    for building in find_all("$.buildings[*]", rmd):
        hvac_zone_list_w_area_dict.update(get_hvac_zone_list_w_area_dict(building))
    return hvac_zone_list_w_area_dict


def get_hvac_zone_list_w_area_dict(building: dict) -> dict[str, HVACZoneListArea]:
    """Gets the list of zones and their total floor area served by each HVAC system
    in a building

    Parameters
    ----------
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema

    Returns
    -------
    dict
        A dictionary of the form
        {
            <hvac_system id>: {
                "zone_list": [<zones served by the hvac system>],
                "total_area": <total area served by the hvac system>
            }
        }
    """
    find_exactly_required_fields(
        GET_HVAC_ZONE_LIST_W_AREA_DICT__REQUIRED_FIELDS["building"], building
    )

    hvac_zone_list_w_area_dict = {}

    for zone in find_all("$.building_segments[*].zones[*]", building):
        terminals = zone.get("terminals")
        # Note: None and [] are falsey; zone.terminals is optional
        if terminals:
            zone_area = sum(find_all("spaces[*].floor_area", zone), ZERO.AREA)
            assert_(zone_area > ZERO.AREA, f"zone:{zone['id']} has zero floor area")
            for terminal in terminals:
                hvac_sys_id = terminal.get(
                    "served_by_heating_ventilating_air_conditioning_system"
                )
                if hvac_sys_id is None:
                    continue

                # Initialize the hvac_sys entry if not already there
                if hvac_sys_id not in hvac_zone_list_w_area_dict:
                    hvac_zone_list_w_area_dict[hvac_sys_id] = {
                        "zone_list": [],
                        "total_area": ZERO.AREA,
                    }

                hvac_sys_entry = hvac_zone_list_w_area_dict[hvac_sys_id]
                if zone["id"] not in hvac_sys_entry["zone_list"]:
                    hvac_sys_entry["zone_list"].append(zone["id"])
                    hvac_sys_entry["total_area"] += zone_area

                assert_(
                    hvac_sys_entry["total_area"] > ZERO.AREA,
                    f"terminal:{terminal['id']} serves zero floor area",
                )
    return hvac_zone_list_w_area_dict
