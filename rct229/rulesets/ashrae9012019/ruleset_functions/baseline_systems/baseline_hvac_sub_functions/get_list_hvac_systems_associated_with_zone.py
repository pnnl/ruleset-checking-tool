from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all


def get_list_hvac_systems_associated_with_zone(rmi, zone_id):
    """
     Get the list of the heating ventilaiton and cooling system ids associated with a zone in either the U_RMD, P_RMD, or B_RMD.

    Parameters
    ----------
    rmi: dict RMI at RuleSetModelInstance level
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
                        "served_by_heating_ventilating_air_conditioning_system",
                        "served_by_heating_ventilating_air_conditioning_system",
                    )
                    for terminal in find_all(
                        f'$.buildings[*].building_segments[*].zones[*][?(@.id="{zone_id}")].terminals[*]',
                        rmi,
                    )
                ]
            )
        )
    )
