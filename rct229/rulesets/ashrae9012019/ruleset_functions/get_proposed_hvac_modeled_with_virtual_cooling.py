from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_one

CoolingSystemOptions = SchemaEnums.schema_enums["CoolingSystemOptions"]

APPLICABLE_COOLING_SYSTEM = [
    CoolingSystemOptions.DIRECT_EXPANSION,
    CoolingSystemOptions.FLUID_LOOP,
    CoolingSystemOptions.NON_MECHANICAL,
    CoolingSystemOptions.OTHER,
]


def get_proposed_hvac_modeled_with_virtual_cooling(
    rmd_u: dict, rmd_p: dict
) -> list[str]:
    """

    Get the list of HeatingVentilatingAirconditioningSystem in which Appendix G Table G3.1 #10 d is applicable (i.e.
    space cooling is modeled in the P_RMD but not the U_RMD). Table G3.1 #10 d states that "where no cooling system
    exists or no cooling system has been submitted with design documents, the cooling system type shall be the same in
    the proposed as modeled in the baseline building design and shall comply with the requirements of Section 6."

    Parameters
    ----------
    rmd_u dict
        A dictionary representing a building as defined by the ASHRAE229 schema. The user RMD to determine if an
        HVAC system has been designed or is existing with cooling.
    rmd_p dict
        A dictionary representing a building as defined by the ASHRAE229 schema. The proposed RMD to determine if the
        same HVAC system has been modeled with cooling in the P-RMD.
    Returns
    -------
    proposed_hvac_modeled_with_virtual_cooling_list list
        A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 d are applicable (i.e. modeled with
        virtual cooling in the proposed).
        Empty list if none
    """
    proposed_hvac_modeled_with_virtual_cooling_list = []
    for hvac_p in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmd_p,
    ):
        cooling_system_type_p = find_one("$.cooling_system.type", hvac_p)
        if cooling_system_type_p in APPLICABLE_COOLING_SYSTEM:
            # cooling system type is found, the hvac_p must have a cooling system
            cooling_system_id = hvac_p["cooling_system"]["id"]
            cooling_system_type_u = find_one(
                f"$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*][?("
                f'@.cooling_system.id="{cooling_system_id}")].cooling_system.type',
                rmd_u,
            )
            if (
                cooling_system_type_u is None
                or cooling_system_type_u == CoolingSystemOptions.NONE
            ):
                proposed_hvac_modeled_with_virtual_cooling_list.append(hvac_p["id"])

    return proposed_hvac_modeled_with_virtual_cooling_list
