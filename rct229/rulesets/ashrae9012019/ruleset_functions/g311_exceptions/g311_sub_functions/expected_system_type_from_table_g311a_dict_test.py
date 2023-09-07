from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.expected_system_type_from_table_g311a_dict import (
    expected_system_type_from_table_g3_1_1_dict,
)
from rct229.schema.config import ureg


def test__expect_system_type_4_public_assembly_cz1a__success():
    # PUBLIC_ASSEMBLY
    # area < 120,000 ft2
    assert expected_system_type_from_table_g3_1_1_dict(
        "PUBLIC_ASSEMBLY", "CZ1A", 3, 110_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_4,
        "system_origin": "PUBLIC_ASSEMBLY CZ_0_to_3a < 120,000 ft2",
    }


def test__expect_system_type_13_public_assembly_cz1a__success():
    assert expected_system_type_from_table_g3_1_1_dict(
        "PUBLIC_ASSEMBLY", "CZ1A", 3, 130_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_13,
        "system_origin": "PUBLIC_ASSEMBLY CZ_0_to_3a >= 120,000 ft2",
    }


def test__expect_system_type_12_public_assembly_cz3b__success():
    assert expected_system_type_from_table_g3_1_1_dict(
        "PUBLIC_ASSEMBLY", "CZ3B", 3, 130_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_12,
        "system_origin": "PUBLIC_ASSEMBLY CZ_3b_3c_or_4_to_8 >= 120,000 ft2",
    }


def test__expect_system_type_5_hospital_cz1a__success():
    # building area <= 150,0000 ft2 AND building has fewer than 5 floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "HOSPITAL", "CZ1A", 3, 130_000 * ureg("ft2")
    ) == {"expected_system_type": HVAC_SYS.SYS_5, "system_origin": "HOSPITAL All Other"}


def test__expect_system_type_7_hospital_cz1a__success():
    # area > 150,000 ft2 OR there are more than 5 floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "HOSPITAL", "CZ1A", 3, 160_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_7,
        "system_origin": "HOSPITAL > 150,000 ft2 or > 5 floors",
    }


def test__expect_system_type_4_retail_cz1a__success():
    # has one or two floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "RETAIL", "CZ1A", 1, 110_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_4,
        "system_origin": "RETAIL CZ_0_to_3a 1 or 2 floors",
    }


def test__expect_system_type_3_retail_cz3b__success():
    # has one or two floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "RETAIL", "CZ3B", 1, 110_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_3,
        "system_origin": "RETAIL CZ_3b_3c_or_4_to_8 1 or 2 floors",
    }


def test__expect_system_type_4_other_non_residential_cz1a__success():
    # area < 25,000 ft2, has fewer than 3 floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ1A", 1, 20_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_4,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_0_to_3a < 25,000 ft2 3 floors or fewer",
    }


def test__expect_system_type_3_other_non_residential_cz3b__success():
    # area < 25,000 ft2, has fewer than 3 floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ3B", 1, 20_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_3,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_3b_3c_or_4_to_8 < 25,000 ft2 3 floors or fewer",
    }


def test__expect_system_type_6_other_non_residential_cz1a__success():
    # area < 25,000 ft2, has 4 or 5 floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ1A", 5, 20_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_6,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_0_to_3a < 25,000 ft2 4-5 floors",
    }


def test__expect_system_type_5_other_non_residential_cz3b__success():
    # area < 25,000 ft2, has 4 or 5 floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ3B", 5, 20_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_5,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_3b_3c_or_4_to_8 < 25,000 ft2 4-5 floors",
    }


def test__expect_system_type_6_other_non_residential_cz1a_5_floors__success():
    # area >= 25,000 ft2 AND <=150,000 ft2, has 5 or fewer floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ1A", 5, 30_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_6,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_0_to_3a >=25,000 ft2 AND <=150,000 ft2 < 6 floors",
    }


def test__expect_system_type_5_other_non_residential_cz3b_5_floors__success():
    # area >= 25,000 ft2 AND <=150,000 ft2, has 5 or fewer floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ3B", 5, 30_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_5,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_3b_3c_or_4_to_8 >=25,000 ft2 AND <=150,000 ft2 < 6 floors",
    }


def test__expect_system_type_8_other_non_residential_cz1a_6_floors__success():
    # area > 150,000 ft2 OR > 5 floors (need to be higher than 25,000 sqft)
    # This case matches to > 5 floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ1A", 6, 30_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_8,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_0_to_3a >150,000 ft2 or > 5 floors",
    }


def test__expect_system_type_8_other_non_residential_cz1a_4_floors__success():
    # area > 150,000 ft2 OR > 5 floors (need to be higher than 25,000 sqft)
    # This case matches to area > 150,000
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ1A", 4, 230_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_8,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_0_to_3a >150,000 ft2 or > 5 floors",
    }


def test__expect_system_type_7_other_non_residential_cz3b_6_floors__success():
    # area > 150,000 ft2 OR > 5 floors (need to be higher than 25,000 sqft)
    # This case matches to > 5 floors
    assert expected_system_type_from_table_g3_1_1_dict(
        "OTHER_NON_RESIDENTIAL", "CZ3B", 6, 30_000 * ureg("ft2")
    ) == {
        "expected_system_type": HVAC_SYS.SYS_7,
        "system_origin": "OTHER_NON_RESIDENTIAL CZ_3b_3c_or_4_to_8 >150,000 ft2 or > 5 floors",
    }
