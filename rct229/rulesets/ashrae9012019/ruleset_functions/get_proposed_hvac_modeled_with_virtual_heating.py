from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_one

HeatingSystemOptions = SchemaEnums.schema_enums["HeatingSystemOptions"]

APPLICABLE_HEATING_SYSTEM = [
    HeatingSystemOptions.HEAT_PUMP,
    HeatingSystemOptions.ELECTRIC_RESISTANCE,
    HeatingSystemOptions.FLUID_LOOP,
    HeatingSystemOptions.OTHER,
]


def get_proposed_hvac_modeled_with_virtual_heating(rmi_u, rmi_p):
    """
    Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 c is applicable (i.e.
    space heating is modeled in the P_RMR but not the U_RMR). Table G3.1 #10 c states that "where no heating system
    exists or no heating system has been submitted with design documents, the system type shall be the same system as
    modeled in the baseline building design and shall comply with but not exceed the requirements of Section 6."

    Parameters
    ----------
    rmi_u dict
        A dictionary representing a building as defined by the ASHRAE229 schema. The user RMI to determine if an
        HVAC system has been designed or is existing with heating.
    rmi_p dict
        A dictionary representing a building as defined by the ASHRAE229 schema. The proposed RMI to determine if the
        same HVAC system has been modeled with heating in the P-RMR.


    Returns
    -------
    proposed_hvac_modeled_with_virtual_heating_list list
        A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 c are applicable (i.e. modeled with
        virtual heating in the proposed).
        Empty list if none
    """
    proposed_hvac_modeled_with_virtual_heating_list = []
    for hvac_p in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmi_p,
    ):
        has_virtual_heating_p = False
        heating_system_type_p = find_one("$.heating_system.type", hvac_p)
        if heating_system_type_p in APPLICABLE_HEATING_SYSTEM:
            # heating system type is found, the hvac_p must have heating system
            heating_system_id = hvac_p["heating_system"]["id"]
            heating_system_type_u = find_one(
                f"$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*][?("
                f'@.heating_system.id="{heating_system_id}")].heating_system.type',
                rmi_u,
            )
            has_virtual_heating_p = (
                heating_system_type_u is None
                or heating_system_type_u == HeatingSystemOptions.NONE
            )

        preheat_system_type_p = find_one("$.preheat_system.type", hvac_p)
        if preheat_system_type_p in APPLICABLE_HEATING_SYSTEM:
            # preheat system type is found, the hvac_p must have preheat system
            preheat_system_id = hvac_p["preheat_system"]["id"]
            preheat_system_type_u = find_one(
                f"$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*][?("
                f'@.preheat_system.id="{preheat_system_id}")].preheat_system.type',
                rmi_u,
            )
            has_virtual_heating_p = (
                has_virtual_heating_p
                or preheat_system_type_u is None
                or preheat_system_type_u == HeatingSystemOptions.NONE
            )

        if has_virtual_heating_p:
            proposed_hvac_modeled_with_virtual_heating_list.append(hvac_p["id"])

    return proposed_hvac_modeled_with_virtual_heating_list
