from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all


def get_list_hvac_systems_associated_with_zone(rmd: dict, zone_id: str) -> list[str]:
    """
     Get the list of the heating ventilation and cooling system ids associated with a zone in either the U_RMD, P_RMD, or B_RMD.

    Parameters
    ----------
    rmd: dict RMD at RuleSetModelDescription level
    zone_id: str Zone id

    Returns: list  A list that saves all the HVAC systems associated with the zone.
    -------

    """
    return sorted(
        list(
            set(
                [
                    getattr_(
                        terminal,
                        "Terminal",
                        "served_by_heating_ventilating_air_conditioning_system",
                    )
                    for terminal in find_all(
                        f'$.buildings[*].building_segments[*].zones[*][?(@.id="{zone_id}")].terminals[*]',
                        rmd,
                    )
                ]
            )
        )
    )
