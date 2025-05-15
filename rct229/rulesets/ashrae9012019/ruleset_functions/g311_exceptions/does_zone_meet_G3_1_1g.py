from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_computer_zones_peak_cooling_load import (
    get_computer_zones_peak_cooling_load,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zones_computer_rooms import (
    get_zone_computer_rooms,
)
from rct229.schema.config import ureg
from rct229.utils.pint_utils import ZERO

COMPUTER_ZONE_PEAK_COOLING_LOAD_THRESHOLD = 600_000 * ureg("Btu/hr")


def does_zone_meet_g3_1_1g(rmd: dict, zone_id: str) -> bool:
    """
    Returns a boolean value indicating whether the zone meets G3_1_1g:

    Parameters
    ----------
    rmd: dict
        A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema
    zone_id: string
        zone id

    Returns
    -------
    True meet exception, false otherwise
    """
    computer_room_zones_dict = get_zone_computer_rooms(rmd)
    total_computer_peak_cooling_load = ZERO.POWER
    if zone_id in computer_room_zones_dict:
        total_computer_peak_cooling_load = get_computer_zones_peak_cooling_load(rmd)
    return total_computer_peak_cooling_load > COMPUTER_ZONE_PEAK_COOLING_LOAD_THRESHOLD
