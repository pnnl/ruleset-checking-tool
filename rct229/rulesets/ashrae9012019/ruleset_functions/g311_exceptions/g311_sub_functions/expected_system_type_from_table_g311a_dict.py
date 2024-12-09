from typing import Literal, Type

import pydash
from pint import Quantity
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.is_cz_0_to_3a_bool import (
    is_cz_0_to_3a_bool,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums

PUBLIC_ASSEMBLY_BUILDING_AREA_THRESHOLD = 120_000 * ureg("ft2")
RETAIL_FLOOR_NUMBER_THRESHOLD = 3
HOSPITAL_BUILDING_AREA_THRESHOLD = 150_000 * ureg("ft2")
HOSPITAL_FLOOR_NUMBER_THRESHOLD = 5
OTHER_NON_RESIDENTIAL_BUILDING_AREA_LOWER_THRESHOLD = 25_000 * ureg("ft2")
OTHER_NON_RESIDENTIAL_BUILDING_AREA_HIGHER_THRESHOLD = 150_000 * ureg("ft2")
OTHER_NON_RESIDENTIAL_FLOOR_NUMBER_LOWER_THRESHOLD = 4
OTHER_NON_RESIDENTIAL_FLOOR_NUMBER_HIGHER_THRESHOLD = 5
HVAC_BUILDING_AREA_TYPE_OPTIONS = SchemaEnums.schema_enums[
    "HeatingVentilatingAirConditioningBuildingAreaOptions2019ASHRAE901"
]

# True message, false message, condition
message_currier = pydash.curry(
    lambda condition, true_input, false_input: true_input if condition else false_input
)


def expected_system_type_from_table_g3_1_1_dict(
    building_area_type: str,
    climate_zone: str,
    number_of_floors: int,
    building_area: Quantity,
) -> dict[Literal["expected_system_type", "system_origin"], [str, Type[HVAC_SYS]]]:
    """

    Parameters
    ----------
    building_area_type: ("RESIDENTIAL", "PUBLIC_ASSEMBLY", "RETAIL", "HOSPITAL", "OTHER_NON_RESIDENTIAL", "HEATED-ONLY_STORAGE")
    climate_zone:
    number_of_floors: this is the number of floors in the building (should be an integer greater than 0)
    building_area: this is the total area of the building

    Returns
    -------
    a dict indicating the expected system type from table G3_1_1 ("SYS-1", "SYS-2", etc)
    and a string that indicates how the system was chosen. An example of the return value:
    {"EXPECTED_SYSTEM_TYPE": "SYS-4", "SYSTEM_ORIGIN": "PUBLIC_ASSEMBLY CZ_0_to_3a < 120,000 ft2"}
    - does not take into account G3.1.1 b-g
    """
    is_cz_0_to_3a_flag = is_cz_0_to_3a_bool(climate_zone)
    climate_zone_currier = message_currier(is_cz_0_to_3a_flag)

    # Initialize the strings
    building_area_string = ""
    number_of_floors_string = ""
    expected_system_type = ""
    climate_zone_category = climate_zone_currier("CZ_0_to_3a", "CZ_3b_3c_or_4_to_8")

    if building_area_type == HVAC_BUILDING_AREA_TYPE_OPTIONS.RETAIL:
        # Retail case - put it on top because this case could change the building_area_type
        if number_of_floors >= RETAIL_FLOOR_NUMBER_THRESHOLD:
            building_area_type = HVAC_BUILDING_AREA_TYPE_OPTIONS.OTHER_NON_RESIDENTIAL
        else:
            number_of_floors_string = message_currier(
                number_of_floors < RETAIL_FLOOR_NUMBER_THRESHOLD, "1 or 2 floors", ""
            )
            expected_system_type = climate_zone_currier(HVAC_SYS.SYS_4, HVAC_SYS.SYS_3)

    if building_area_type == HVAC_BUILDING_AREA_TYPE_OPTIONS.RESIDENTIAL:
        # Residential case
        expected_system_type = climate_zone_currier(HVAC_SYS.SYS_2, HVAC_SYS.SYS_1)
    if building_area_type == HVAC_BUILDING_AREA_TYPE_OPTIONS.PUBLIC_ASSEMBLY:
        # Public assembly case
        public_assembly_area_currier = message_currier(
            building_area < PUBLIC_ASSEMBLY_BUILDING_AREA_THRESHOLD
        )
        building_area_string = public_assembly_area_currier(
            "< 120,000 ft2", ">= 120,000 ft2"
        )

        # true, sys 4 or sys3, false sys 13 or sys 12.
        expected_system_type = public_assembly_area_currier(
            climate_zone_currier(HVAC_SYS.SYS_4, HVAC_SYS.SYS_3),
            climate_zone_currier(HVAC_SYS.SYS_13, HVAC_SYS.SYS_12),
        )

    if building_area_type == HVAC_BUILDING_AREA_TYPE_OPTIONS.HEATED_ONLY_STORAGE:
        # Heated only storage case
        expected_system_type = climate_zone_currier(HVAC_SYS.SYS_10, HVAC_SYS.SYS_9)

    if building_area_type == HVAC_BUILDING_AREA_TYPE_OPTIONS.HOSPITAL:
        # Reset the climate zone category because hospital does not require climate zone
        climate_zone_category = ""
        hospital_area_currier = message_currier(
            building_area > HOSPITAL_BUILDING_AREA_THRESHOLD
            or number_of_floors > HOSPITAL_FLOOR_NUMBER_THRESHOLD
        )

        building_area_string = hospital_area_currier(
            "> 150,000 ft2 or > 5 floors", "All Other"
        )
        expected_system_type = hospital_area_currier(HVAC_SYS.SYS_7, HVAC_SYS.SYS_5)

    if building_area_type == HVAC_BUILDING_AREA_TYPE_OPTIONS.OTHER_NON_RESIDENTIAL:
        building_area_low_area_flag = (
            building_area < OTHER_NON_RESIDENTIAL_BUILDING_AREA_LOWER_THRESHOLD
        )
        building_area_medium_area_flag = (
            OTHER_NON_RESIDENTIAL_BUILDING_AREA_LOWER_THRESHOLD
            <= building_area
            <= OTHER_NON_RESIDENTIAL_BUILDING_AREA_HIGHER_THRESHOLD
        )
        building_area_large_area_flag = (
            building_area > OTHER_NON_RESIDENTIAL_BUILDING_AREA_HIGHER_THRESHOLD
        )
        number_of_floors_low_flag = (
            number_of_floors < OTHER_NON_RESIDENTIAL_FLOOR_NUMBER_LOWER_THRESHOLD
        )
        number_of_floors_medium_flag = (
            number_of_floors <= OTHER_NON_RESIDENTIAL_FLOOR_NUMBER_HIGHER_THRESHOLD
        )
        number_of_floors_high_flag = (
            number_of_floors > OTHER_NON_RESIDENTIAL_FLOOR_NUMBER_HIGHER_THRESHOLD
        )

        # building area string
        if building_area_low_area_flag:
            # building_area < 25000
            building_area_string = "< 25,000 ft2"
            if number_of_floors_low_flag:
                number_of_floors_string = "3 floors or fewer"
                expected_system_type = climate_zone_currier(
                    HVAC_SYS.SYS_4, HVAC_SYS.SYS_3
                )
            elif number_of_floors_medium_flag:
                number_of_floors_string = "4-5 floors"
                expected_system_type = climate_zone_currier(
                    HVAC_SYS.SYS_6, HVAC_SYS.SYS_5
                )
        elif building_area_medium_area_flag and number_of_floors_medium_flag:
            # (building_area >= 25000) && (building_area < 150000) && (number_of_floors <= 5)
            building_area_string = ">=25,000 ft2 AND <=150,000 ft2"
            number_of_floors_string = "< 6 floors"
            expected_system_type = climate_zone_currier(HVAC_SYS.SYS_6, HVAC_SYS.SYS_5)
        elif building_area_large_area_flag or number_of_floors_high_flag:
            # (building_area > 150000) || (number_of_floors > 5)
            building_area_string = ">150,000 ft2 or > 5 floors"
            expected_system_type = climate_zone_currier(HVAC_SYS.SYS_8, HVAC_SYS.SYS_7)

    details_of_system_selection = f"{building_area_type} {climate_zone_category} {building_area_string} {number_of_floors_string}"
    return {
        "expected_system_type": expected_system_type,
        "system_origin": " ".join(details_of_system_selection.split()),
    }
