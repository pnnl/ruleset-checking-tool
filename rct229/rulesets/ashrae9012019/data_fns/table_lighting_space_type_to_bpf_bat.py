from rct229.rulesets.ashrae9012019.data import data
from rct229.utils.assertions import assert_


def lighting_space_type_to_bpf_bat(lgt_space_type):
    lgt_space_type_to__bpf_bat = data["ashrae_90_1_lighting_space_type_bpf_bat"]
    assert_(
        lgt_space_type in lgt_space_type_to__bpf_bat,
        f"Lighting space type {lgt_space_type} does not exist in ashrae_90_1_lighting_space_type_bpf_bat",
    )

    return lgt_space_type_to__bpf_bat[lgt_space_type]
