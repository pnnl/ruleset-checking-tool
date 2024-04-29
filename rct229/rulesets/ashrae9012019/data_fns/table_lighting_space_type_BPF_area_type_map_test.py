from rct229.rulesets.ashrae9012019.data_fns.table_lighting_space_type_BPF_area_type_map import (
    lighting_space_type_to_BPF_area_type,
)


def test__lighting_to_BPF_area_type__AUTOMOTIVE_FACILITY():
    assert lighting_space_type_to_BPF_area_type("AUTOMOTIVE_FACILITY") == "ALL_OTHER"


def test__lighting_to_BPF_area_type__DINING_BAR_LOUNGE_LEISURE():
    assert (
        lighting_space_type_to_BPF_area_type("DINING_BAR_LOUNGE_LEISURE")
        == "RESTAURANT"
    )


def test__lighting_to_BPF_area_type__HEALTH_CARE_CLINIC():
    assert (
        lighting_space_type_to_BPF_area_type("HEALTH_CARE_CLINIC")
        == "HEALTHCARE_HOSPITAL"
    )


def test__lighting_to_BPF_area_type__NONE():
    assert lighting_space_type_to_BPF_area_type("NONE") == "NONE"
