from rct229.rulesets.ashrae9012019.data_fns.table_lighting_space_type_to_bpf_bat import (
    lighting_space_type_to_bpf_bat,
)


def test__lighting_to_hvac_bat__ATRIUM_HIGH():
    assert lighting_space_type_to_bpf_bat("ATRIUM_HIGH") == "UNDETERMINED"


def test__space_lighting_to_hvac_bat__AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER():
    assert (
        lighting_space_type_to_bpf_bat("AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER")
        == "ALL_OTHER"
    )


def test__space_lighting_to_hvac_bat__LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY():
    assert (
        lighting_space_type_to_bpf_bat("LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY")
        == "HEALTHCARE_HOSPITAL"
    )


def test__space_lighting_to_hvac_bat__DORMITORY_LIVING_QUARTERS():
    assert lighting_space_type_to_bpf_bat("DORMITORY_LIVING_QUARTERS") == "MULTIFAMILY"


def test__space_lighting_to_hvac_bat__WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS():
    assert (
        lighting_space_type_to_bpf_bat(
            "WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS"
        )
        == "WAREHOUSE"
    )
