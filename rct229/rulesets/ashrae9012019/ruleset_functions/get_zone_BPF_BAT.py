from pint import Quantity
from rct229.rulesets.ashrae9012019.data_fns.table_lighting_space_type_to_bpf_bat import (
    lighting_space_type_to_bpf_bat,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO


def get_zone_BPF_BAT(rmd: dict, zone_id: str) -> dict[str, Quantity]:
    """
     Get a dictionary of the BPF_BAT and areas for a given zone.

     Parameters
    ----------
    RMD: str, The ruleset model descriptions
    zone_id: str, The id of the zone

    Returns
    -------
    zone_BPF_BAT_dict: A dict for the zone that saves the BPF_BAT as keys and the areas as the values.
                       Example: {SCHOOL: 50000, UNDETERMINED: 2000}

    """

    zone_BPF_BAT_dict = {}
    for space in find_all(
        f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id}")].spaces[*]',
        rmd,
    ):
        lighting_space_type = space.get("lighting_space_type", None)
        space_BPF_BAT = (
            "UNDETERMINED"
            if lighting_space_type is None
            else lighting_space_type_to_bpf_bat(lighting_space_type)
        )

        if space_BPF_BAT in zone_BPF_BAT_dict:
            zone_BPF_BAT_dict[space_BPF_BAT] += space.get("floor_area", ZERO.AREA)
        else:
            zone_BPF_BAT_dict[space_BPF_BAT] = space.get("floor_area", ZERO.AREA)

    assert_(
        zone_BPF_BAT_dict,
        f"No spaces have been found in zone `{zone_id}`. Check the RPD inputs.",
    )

    return zone_BPF_BAT_dict
