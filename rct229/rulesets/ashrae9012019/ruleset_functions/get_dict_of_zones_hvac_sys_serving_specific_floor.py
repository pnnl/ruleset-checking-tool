from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.jsonpath_utils import find_all


def get_dict_of_zones_hvac_sys_serving_specific_floor(rmi, floor_name):
    """
    Returns a dictionary with zone ids as the keys and the associated HVAC system as the values for zones serving a specific floor the applicable RMR i.e. {zone_1.id: [hvac_1.id, hvac_2.id, hvac_3.id], zone_2.id: [hvac_1.id, hvac_2.id, hvac_3.id]}.

    Parameters
    ----------
    floor_name: A floor name (string) associated with the RMR to determine the zone ids and hvac systems that are associated with the specific floor.
    rmi: dict rmd at RuleSetModelInstance level.
    Returns:
    dict_of_zones_hvac_sys_serving_specific_floor: a dictionary with zone ids as the keys and the associated HVAC system as the values for zones serving a specific floor the applicable RMR i.e. {zone_1.id: [hvac_1.id, hvac_2.id, hvac_3.id], zone_2.id: [hvac_1.id, hvac_2.id, hvac_3.id]}.

    """
    dict_of_zones_hvac_sys_serving_specific_floor = {}
    for zone_id in find_all(
        f'$.buildings[*].building_segments[*].zones[*][?(@.floor_name ="{floor_name}")].id',
        rmi,
    ):
        dict_of_zones_hvac_sys_serving_specific_floor[
            zone_id
        ] = get_list_hvac_systems_associated_with_zone(rmi, zone_id)

    return dict_of_zones_hvac_sys_serving_specific_floor
