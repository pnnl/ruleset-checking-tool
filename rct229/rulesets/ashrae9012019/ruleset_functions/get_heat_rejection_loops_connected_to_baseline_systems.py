from rct229.rulesets.ashrae9012019.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.utils.jsonpath_utils import find_all, find_one


def get_heat_rejection_loops_connected_to_baseline_systems(rmd: dict) -> list:
    """
    Get a list of all heat rejection loops in an RMD that are connected to a baseline HVAC System (Type-7, 8, 11.1,
    11.2, 12, 13, 7b, 8b, 11.1b, 12b)

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema

    Returns -------
    heat_reject_loop_list list
        A list saves the ids of heat rejection loops in the model that serve baseline system types. If no qualifying
        heat rejection loops, return an empty list.
    """
    primary_secondary_loops_dict = get_primary_secondary_loops_dict(rmd)
    heat_rejection_loop_list = [
        chiller["condensing_loop"]
        for chiller in find_all("$.chillers[*]", rmd)
        if find_one("$.cooling_loop", chiller) in primary_secondary_loops_dict
        and chiller.get("condensing_loop")
    ]
    return list(set(heat_rejection_loop_list))
