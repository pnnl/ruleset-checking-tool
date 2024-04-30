from rct229.rulesets.ashrae9012019.data import data
from rct229.utils.assertions import assert_


def lighting_space_type_to_BPF_area_type(lighting_space_type):
    lgt_space_type_BPF_area_type = data["ashrae_90_1_lighting_space_type_BPF_area_type"]
    assert_(
        lighting_space_type in lgt_space_type_BPF_area_type,
        f"Lighting area type {lighting_space_type} does not exist in ashrae_90_1_lighting_to_hvac_map",
    )
    return lgt_space_type_BPF_area_type[lighting_space_type]
