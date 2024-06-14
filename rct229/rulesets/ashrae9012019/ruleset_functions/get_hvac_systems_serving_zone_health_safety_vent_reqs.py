from functools import reduce
from operator import concat

from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

LightingSpaceOptionsG37 = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]
VentilationSpaceOptions = SchemaEnums.schema_enums[
    "VentilationSpaceOptions2019ASHRAE901"
]

LIGHTING_SPACE_TYPES_MATCH_REQ = [
    LightingSpaceOptionsG37.MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA,
    LightingSpaceOptionsG37.MANUFACTURING_FACILITY_EQUIPMENTROOM,
    LightingSpaceOptionsG37.HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM,
    LightingSpaceOptionsG37.HEALTHCARE_FACILITY_MEDICAL_SUPPLY_ROOM,
    LightingSpaceOptionsG37.HEALTHCARE_FACILITY_NURSERY,
    LightingSpaceOptionsG37.HEALTHCARE_FACILITY_OPERATING_ROOM,
    LightingSpaceOptionsG37.HEALTHCARE_FACILITY_PATIENT_ROOM,
    LightingSpaceOptionsG37.HEALTHCARE_FACILITY_RECOVERY_ROOM,
    LightingSpaceOptionsG37.MUSEUM_RESTORATION_ROOM,
    LightingSpaceOptionsG37.PHARMACY_AREA,
    LightingSpaceOptionsG37.EMERGENCY_VEHICLE_GARAGE,
    LightingSpaceOptionsG37.CONFINEMENT_CELLS,
]

VENTILATION_SPACE_TYPES_MATCH_REQ = [
    VentilationSpaceOptions.OUTPATIENT_HEALTH_CARE_FACILITIES_CLASS_1_IMAGING_ROOMS,
    VentilationSpaceOptions.ANIMAL_FACILITIES_ANIMAL_IMAGING_MRI_CT_PET,
]


def get_hvac_systems_serving_zone_health_safety_vent_reqs(rmd: dict) -> list[str]:
    """
    Get the list of HVAC systems that are likely to serve zones that have health and safety mandated minimum
    ventilation requirements during unoccupied hours.

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema.

        To determine if any of the zones have spaces with lighting spaces types that are likely to have health and
        safety mandated minimum ventilation requirements during unoccupied hours and to create a list of the hvac
        systems associated with these zones.

    Returns
    -------
    hvac_systems_unocc_health_safety_vent_list list
        A list that saves all hvac systems that are likely to serve zones that have health and safety mandated
        minimum ventilation requirements during unoccupied hours.
    """
    applicable_zone_ids_list = [
        zone["id"]
        for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmd)
        if any(
            [
                space.get("lighting_space_type") in LIGHTING_SPACE_TYPES_MATCH_REQ
                or space.get("ventilation_space_type")
                in VENTILATION_SPACE_TYPES_MATCH_REQ
                for space in find_all("$.spaces[*]", zone)
            ]
        )
    ]

    hvac_lists = [
        get_list_hvac_systems_associated_with_zone(rmd, zone_id)
        for zone_id in applicable_zone_ids_list
    ]
    # len(hvac_lists) > 0 This does not guarantee the result won't be an empty list
    # e.g., [[]] -> []
    return list(set(reduce(concat, hvac_lists))) if len(hvac_lists) > 0 else []
