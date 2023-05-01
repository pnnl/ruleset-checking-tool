from rct229.utils.assertions import assert_, assert_required_fields
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, pint_sum

# Intended for export and internal use
GET_HVAC_ZONE_LIST_W_AREA_DICT__REQUIRED_FIELDS = {
    "building": {
        "building_segments[*].zones[*].spaces[*]": [
            "floor_area",
        ],
        "building_segments[*].zones[*].terminals[*]": [
            "served_by_heating_ventilating_air_conditioning_system"
        ],
    }
}


def get_hvac_zone_list_w_area_by_rmi_dict(rmi):
    """
    RMI version of the get_hvac_zone_list_w_area_dict function

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema

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
    for building in find_all("$.buildings[*]", rmi):
        hvac_zone_list_w_area_dict.update(get_hvac_zone_list_w_area_dict(building))
    return hvac_zone_list_w_area_dict


def get_hvac_zone_list_w_area_dict(building):
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
    assert_required_fields(
        GET_HVAC_ZONE_LIST_W_AREA_DICT__REQUIRED_FIELDS["building"], building
    )

    hvac_zone_list_w_area_dict = {}

    for zone in find_all("$.building_segments[*].zones[*]", building):
        terminals = zone.get("terminals")
        # Note: None and [] are falsey; zone.terminals is optional
        if terminals:
            zone_area = pint_sum(find_all("spaces[*].floor_area", zone), ZERO.AREA)
            assert_(zone_area > ZERO.AREA, f"zone:{zone['id']} has zero floor area")
            for terminal in terminals:
                hvac_sys_id = terminal[
                    "served_by_heating_ventilating_air_conditioning_system"
                ]

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
