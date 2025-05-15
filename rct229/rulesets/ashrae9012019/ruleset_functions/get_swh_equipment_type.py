from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

SERVICE_WATER_HEATER_TANK = SchemaEnums.schema_enums["ServiceWaterHeaterTankOptions"]
ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]

INSTANTANEOUS_TYPE = [
    SERVICE_WATER_HEATER_TANK.CONSUMER_INSTANTANEOUS,
    SERVICE_WATER_HEATER_TANK.COMMERCIAL_INSTANTANEOUS,
    SERVICE_WATER_HEATER_TANK.RESIDENTIAL_DUTY_COMMERCIAL_INSTANTANEOUS,
]
STORAGE_TYPE = [
    SERVICE_WATER_HEATER_TANK.CONSUMER_STORAGE,
    SERVICE_WATER_HEATER_TANK.COMMERCIAL_STORAGE,
]


class GetSWHEquipmentType:
    ELECTRIC_RESISTANCE_INSTANTANEOUS = "ELECTRIC_RESISTANCE_INSTANTANEOUS"
    ELECTRIC_RESISTANCE_STORAGE = "ELECTRIC_RESISTANCE_STORAGE_WATER_HEATER"
    GAS_INSTANTANEOUS = "GAS_INSTANTANEOUS"
    GAS_STORAGE = "GAS_STORAGE_WATER_HEATER"
    OIL_INSTANTANEOUS = "OIL_INSTANTANEOUS"
    OIL_STORAGE = "OIL_STORAGE_WATER_HEATER"
    PROPANE_INSTANTANEOUS = "PROPANE_INSTANTANEOUS"
    PROPANE_STORAGE = "PROPANE_STORAGE"
    OTHER = "OTHER"


def get_swh_equipment_type(rmd: dict, service_water_heating_equipment_id: str) -> str:
    """
    This function determines whether the swh equipment type is one of: (ELECTRIC_RESISTANCE_INSTANTANEOUS, ELECTRIC_RESISTANCE_STORAGE, GAS_STORAGE, PROPANE_INSTANTANEOUS, PROPANE_STORAGE, OTHER)

    Parameters
    ----------
    rmd: dict
        RMD at RuleSetModelDescription level
    service_water_heating_equipment_id: str
        service water heating equipment id

    Returns
    -------
    type: string
        ex: type = "ELECTRIC_RESISTANCE_INSTANTANEOUS"
    """

    service_water_heating_equipment = find_exactly_one_with_field_value(
        "$.service_water_heating_equipment[*]",
        "id",
        service_water_heating_equipment_id,
        rmd,
    )

    swh_tank_type = getattr_(
        service_water_heating_equipment,
        "service_water_heating_equipment",
        "tank",
        "type",
    )
    compressor_heat_rejection_source = service_water_heating_equipment.get(
        "compressor_heat_rejection_source"
    )
    compressor_capacity_validation_points = service_water_heating_equipment.get(
        "compressor_capacity_validation_points"
    )
    compressor_power_validation_points = service_water_heating_equipment.get(
        "compressor_power_validation_points"
    )
    swh_type = (
        "CONVENTIONAL"
        if not compressor_heat_rejection_source
        and not compressor_capacity_validation_points
        and not compressor_power_validation_points
        else "HEAT PUMP"
    )
    fuel_type = getattr_(
        service_water_heating_equipment,
        "service_water_heating_equipment",
        "heater_fuel_type",
    )

    assert_(
        fuel_type
        in [
            ENERGY_SOURCE.ELECTRICITY,
            ENERGY_SOURCE.NATURAL_GAS,
            ENERGY_SOURCE.PROPANE,
            ENERGY_SOURCE.FUEL_OIL,
        ],
        "Fuel type must be one of `ELECTRICITY`, `NATURAL_GAS`, `PROPANE`, `FUEL_OIL`.",
    )

    if swh_type == "CONVENTIONAL":
        if swh_tank_type in INSTANTANEOUS_TYPE:
            if fuel_type == ENERGY_SOURCE.ELECTRICITY:
                type = GetSWHEquipmentType.ELECTRIC_RESISTANCE_INSTANTANEOUS
            elif fuel_type == ENERGY_SOURCE.NATURAL_GAS:
                type = GetSWHEquipmentType.GAS_INSTANTANEOUS
            elif fuel_type == ENERGY_SOURCE.PROPANE:
                type = GetSWHEquipmentType.PROPANE_INSTANTANEOUS
            elif fuel_type == ENERGY_SOURCE.FUEL_OIL:
                type = GetSWHEquipmentType.OIL_INSTANTANEOUS

        elif swh_tank_type in STORAGE_TYPE:
            if fuel_type == ENERGY_SOURCE.ELECTRICITY:
                type = GetSWHEquipmentType.ELECTRIC_RESISTANCE_STORAGE
            elif fuel_type == ENERGY_SOURCE.NATURAL_GAS:
                type = GetSWHEquipmentType.GAS_STORAGE
            elif fuel_type == ENERGY_SOURCE.PROPANE:
                type = GetSWHEquipmentType.PROPANE_STORAGE
            elif fuel_type == ENERGY_SOURCE.FUEL_OIL:
                type = GetSWHEquipmentType.OIL_STORAGE
    else:
        type = GetSWHEquipmentType.OTHER

    return type
