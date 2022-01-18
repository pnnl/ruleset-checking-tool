from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import pint_sum


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
    hvac_zone_list_w_area_dict = {}

    for zone in find_all("$..zones[*]", building):
        terminals = zone.get("terminals")
        # Note: None and [] are falsey
        if terminals:
            zone_area = pint_sum(find_all("spaces[*].floor_area", zone))
            for terminal in zone.terminals:
                hvac_sys_id = terminal[
                    "served_by_heating_ventialtion_air_conditiong_systems"
                ]

                # Initialize the hvac_sys entry if not already there
                if hvac_sys_id not in hvac_zone_list_w_area_dict:
                    hvac_zone_list_w_area_dict[hvac_sys_id] = {
                        "zone_list": [],
                        "total_area": 0,
                    }

                hvac_sys_entry = hvac_zone_list_w_area_dict[hvac_sys_id]
                if zone["id"] not in zone_list:
                    hvac_sys_entry["zone_list"].append(zone["id"])
                    hvac_sys_entry["total_area"] += zone_area

    return hvac_zone_list_w_area_dict
