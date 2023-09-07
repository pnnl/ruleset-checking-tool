from rct229.schema.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_all

SpaceFunctionOptions = schema_enums["SpaceFunctionOptions"]


def get_building_lab_zones_list(rmi):
    """
    returns a list of all of the zones in the building that include a laboratory space

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema

    Returns
    -------
    a list of zone.ids for all zones that have a laboratory space in the building
    """
    laboratory_zone_list = []
    for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmi):
        if any(
            [
                space.get("function") == SpaceFunctionOptions.LABORATORY
                for space in find_all("$.spaces[*]", zone)
            ]
        ):
            laboratory_zone_list.append(zone["id"])

    return laboratory_zone_list
