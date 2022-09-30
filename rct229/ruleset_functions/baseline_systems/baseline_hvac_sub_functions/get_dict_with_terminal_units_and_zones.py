from rct229.utils.jsonpath_utils import find_all


def get_dict_with_terminal_units_and_zones(rmi):
    terminal_units_and_zones_dict = {}
    for terminal in find_all("$..terminals[*]", rmi):
        terminal_id = terminal["id"]
        terminal_units_and_zones_dict[terminal_id] = find_all(
            # search all zones that have terminal(s) match to this terminal id
            # and return them in a list.
            f'$..zones[*][?(@.terminals[*].id="{terminal_id}")].id',
            rmi,
        )
    return terminal_units_and_zones_dict
