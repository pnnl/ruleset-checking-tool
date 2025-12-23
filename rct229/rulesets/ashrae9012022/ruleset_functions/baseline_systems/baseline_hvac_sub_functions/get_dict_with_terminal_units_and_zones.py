from rct229.utils.jsonpath_utils import find_all


def get_dict_with_terminal_units_and_zones(rmd: dict) -> dict:
    """
    Returns a dictionary of zone IDs associated with each terminal unit in the RMD.

    Parameters
    ----------
    rmd: json

    Returns ------- dict a dictionary of zones associated with each terminal unit in the rmd, {terminal_unit_1.id: [
    zone_1.id, zone_2.id, zone_3.id], terminal_unit_2.id: [zone_4.id, zone_9.id, zone_30.id]}

    """
    return {
        terminal["id"]: find_all(
            # search all zones that have terminal(s) match to this terminal id
            # and return them in a list.
            f'$.buildings[*].building_segments[*].zones[*][?(@.terminals[*].id="{terminal["id"]}")].id',
            rmd,
        )
        for terminal in find_all(
            "$.buildings[*].building_segments[*].zones[*].terminals[*]", rmd
        )
    }
