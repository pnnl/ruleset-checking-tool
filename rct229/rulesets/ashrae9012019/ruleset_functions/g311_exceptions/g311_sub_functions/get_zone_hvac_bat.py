from pint import Quantity
from rct229.rulesets.ashrae9012019.data_fns.table_lighting_to_hvac_bat_map_fns import (
    space_lighting_to_hvac_bat,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_zone


def get_zone_hvac_bat_dict(rmd: dict, zone_id: str) -> dict[str, Quantity]:
    """
    Get a dictionary of the HVAC_BAT and areas for a given zone.
        - used to verify the correct type of HVAC baseline system (or systems)
        - The function looks at the space lighting type.

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    zone_hvac_bat_dict dict A dict for the zone that saves the HVAC_BAT as keys and the areas as the
    values. Example: {OTHER_NON_RESIDENTIAL: 500, PUBLIC_ASSEMBLY: 2000}

    """
    zone_hvac_bat_dict = dict()
    zone = find_exactly_one_zone(rmd, zone_id)
    for space in find_all("$.spaces[*]", zone):
        # set default to None to not fail the data retrieving (space could have no lighting space type)
        space_hvac_bat = space_lighting_to_hvac_bat(
            space.get("lighting_space_type", "NONE")
        )
        # Default missing floor area to ZERO Area
        zone_hvac_bat_dict[space_hvac_bat] = zone_hvac_bat_dict.get(
            space_hvac_bat, ZERO.AREA
        ) + space.get("floor_area", ZERO.AREA)
    return zone_hvac_bat_dict
