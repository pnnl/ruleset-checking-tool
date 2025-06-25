import json
import os
from collections import Counter
from referencing import Registry
from jsonschema import Draft7Validator
from referencing.jsonschema import DRAFT7

from rct229.schema.schema_store import SchemaStore
from rct229.utils.jsonpath_utils import (
    find_all,
    find_all_by_jsonpaths,
    convert_absolute_path_list_to_jsonpath,
    format_jsonpath_with_id,
)

file_dir = os.path.dirname(__file__)

SCHEMA_KEY = SchemaStore.SCHEMA_KEY
SCHEMA_ENUM_KEY = SchemaStore.SCHEMA_9012019_ENUM_KEY
SCHEMA_RESNET_ENUM_KEY = SchemaStore.SCHEMA_RESNET_ENUM_KEY
SCHEMA_T24_ENUM_KEY = SchemaStore.SCHEMA_T24_ENUM_KEY
SCHEMA_OUTPUT_KEY = SchemaStore.SCHEMA_9012019_OUTPUT_KEY
SCHEMA_PATH = os.path.join(file_dir, SCHEMA_KEY)
SCHEMA_ENUM_PATH = os.path.join(file_dir, SCHEMA_ENUM_KEY)
SCHEMA_T24_ENUM_PATH = os.path.join(file_dir, SCHEMA_T24_ENUM_KEY)
SCHEMA_RESNET_ENUM_PATH = os.path.join(file_dir, SCHEMA_RESNET_ENUM_KEY)
SCHEMA_OUTPUT_PATH = os.path.join(file_dir, SCHEMA_OUTPUT_KEY)


def check_associated_data_elements(rpd: dict) -> list[str]:
    """
    Check validity of separate data elements that are associated with each other.
    e.g. if SWH use is populated, SWH use_units must also be populated.
    e.g. if efficiency_metric_values is populated, it must have the same length as efficiency_metric_types

    Parameters
    ----------
    rpd

    Returns list of object ids where the associated lists are not the same length
    -------

    """
    mismatch_errors = []

    associated_list_data_elements = [
        ("use_units", "use"),
        ("efficiency_metric_types", "efficiency_metric_values"),
    ]
    associated_list_jsonpaths = [
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].heating_system",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].preheat_system",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].cooling_system",
        "$.ruleset_model_descriptions[*].boilers[*]",
        "$.ruleset_model_descriptions[*].chillers[*]",
        "$.ruleset_model_descriptions[*].service_water_heating_equipment[*]",
        "$.ruleset_model_descriptions[*].service_water_heating_uses[*]",
    ]

    for jsonpath in associated_list_jsonpaths:
        object_list = find_all(jsonpath, rpd)

        for obj in object_list:
            for key_1, key_2 in associated_list_data_elements:
                val_1, val_2 = obj.get(key_1, None), obj.get(key_2, None)
                if val_1 is None and val_2 is None:
                    continue
                # XOR operation
                if (val_1 is None) != (val_2 is None):
                    mismatch_errors.append(
                        f"'{obj['id']}' has populated '{key_1 if val_1 else key_2}' but is missing '{key_1 if not val_1 else key_2}'."
                    )
                    continue

                # Ensure when both are lists they have the same length
                if isinstance(val_1, list) and isinstance(val_2, list):
                    val_1, val_2 = obj[key_1], obj[key_2]
                    if val_1 and val_2 and len(val_1) != len(val_2):
                        mismatch_errors.append(
                            f"'{obj['id']}' lists at '{key_1}' and '{key_2}' are not the same length."
                        )

    return mismatch_errors


def check_fluid_loop_association(rpd: dict) -> list:
    """
    Check the association between fluid loops and the various objects which reference them.
    Parameters
    ----------
    rpd

    Returns list of mismatched fluid loop ids
    -------

    """
    mismatch_list = []

    fluid_loop_id_jsonpaths = [
        "$.ruleset_model_descriptions[*].fluid_loops[*].id",
        "$.ruleset_model_descriptions[*].fluid_loops[*].child_loops[*].id",
    ]

    fluid_reference_jsonpaths = [
        "$.ruleset_model_descriptions[*].chillers[*].cooling_loop",
        "$.ruleset_model_descriptions[*].chillers[*].condensing_loop",
        "$.ruleset_model_descriptions[*].chillers[*].heat_recovery_loop",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].heating_system.hot_water_loop",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].heating_system.water_source_heat_pump_loop",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].cooling_system.chilled_water_loop",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].cooling_system.condenser_water_loop",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].energy_from_loop",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].remaining_fraction_to_loop",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].terminals[*].cooling_from_loop",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].terminals[*].heating_from_loop",
        "$.ruleset_model_descriptions[*].service_water_heating_equipment[*].hot_water_loop",
        "$.ruleset_model_descriptions[*].heat_rejections[*].loop",
        "$.ruleset_model_descriptions[*].boilers[*].loop",
        "$.ruleset_model_descriptions[*].service_water_heating_equipment[*].hot_water_loop",
        "$.ruleset_model_descriptions[*].external_fluid_sources[*].loop",
    ]

    fluid_loop_id_list = find_all_by_jsonpaths(fluid_loop_id_jsonpaths, rpd)

    referenced_id_list = find_all_by_jsonpaths(
        fluid_reference_jsonpaths,
        rpd,
    )

    for fluid_loop_id in referenced_id_list:
        if fluid_loop_id not in fluid_loop_id_list:
            mismatch_list.append(fluid_loop_id)

    return mismatch_list


def check_zone_association(rpd: dict) -> list:
    """
    Check the association between zones and the various objects which reference them.
    Parameters
    ----------
    rpd

    Returns list of mismatched zone ids
    -------

    """
    mismatch_list = []
    zone_reference_jsonpaths = [
        "$.ruleset_model_descriptions[*].buildings[*].elevators[*].motor_location_zone",
        "$.ruleset_model_descriptions[*].buildings[*].elevators[*].cab_location_zone",
        "$.ruleset_model_descriptions[*].buildings[*].refrigerated_cases[*].zone",
        "$.ruleset_model_descriptions[*].service_water_heating_equipment[*].compressor_zone",
        "$.ruleset_model_descriptions[*].service_water_heating_equipment[*].compressor_heat_rejection_zone",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].zonal_exhaust_fan.motor_location_zone",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].terminals[*].fan.motor_location_zone",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].fan_system.supply_fans[*].motor_location_zone",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].fan_system.return_fans[*].motor_location_zone",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].fan_system.relief_fans[*].motor_location_zone",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].fan_system.exhaust_fans[*].motor_location_zone",
        "$.ruleset_model_descriptions[*].service_water_heating_equipment[*].tank.location_zone",
        "$.ruleset_model_descriptions[*].service_water_heating_equipment[*].solar_thermal_systems[*].tank.location_zone",
        "$.ruleset_model_descriptions[*].service_water_heating_distribution_systems[*].tanks[*].location_zone",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].surfaces[*].adjacent_zone",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].transfer_airflow_source_zone",
        "$.ruleset_model_descriptions[*].service_water_heating_distribution_systems[*].service_water_piping[*].location_zone",
    ]
    zone_id_list = find_all(
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].id",
        rpd,
    )
    referenced_id_list = find_all_by_jsonpaths(zone_reference_jsonpaths, rpd)

    for zone_id in referenced_id_list:
        if zone_id not in zone_id_list:
            mismatch_list.append(zone_id)
    return mismatch_list


def check_schedule_association(rpd: dict) -> list:
    """
    Check the association between schedules and the various objects which reference them.
    Parameters
    ----------
    rpd

    Returns list of mismatched schedule ids
    -------

    """
    mismatch_list = []

    schedule_id_list = find_all("$.ruleset_model_descriptions[*].schedules[*].id", rpd)
    schedule_reference_jsonpaths = [
        "$.ruleset_model_descriptions[*].buildings[*].elevators[*].cab_motor_multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].elevators[*].cab_ventilation_fan_multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].elevators[*].cab_lighting_multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].refrigerated_cases[*].power_multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].exterior_lighting[*].multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].infiltration.multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].thermostat_cooling_setpoint_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].thermostat_heating_setpoint_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].minimum_humidity_setpoint_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].maximum_humidity_setpoint_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].exhaust_airflow_rate_multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].spaces[*].occupant_multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].spaces[*].interior_lighting[*].lighting_multiplier_schedule",
        "$.ruleset_model_descriptions[*].service_water_heating_distribution_systems[*].flow_multiplier_schedule",
        "$.ruleset_model_descriptions[*].service_water_heating_distribution_systems[*].entering_water_mains_temperature_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*].use_multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_open_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].terminals[*].minimum_outdoor_airflow_multiplier_schedule",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].multiplier_schedule",
        "$.ruleset_model_descriptions[*].fluid_loops[*].cooling_or_condensing_design_and_control.operation_schedule",
        "$.ruleset_model_descriptions[*].fluid_loops[*].heating_design_and_control.operation_schedule",
        "$.ruleset_model_descriptions[*].fluid_loops[*].child_loops[*].cooling_or_condensing_design_and_control.operation_schedule",
        "$.ruleset_model_descriptions[*].fluid_loops[*].child_loops[*].heating_design_and_control.operation_schedule",
        "$.ruleset_model_descriptions[*].heating_ventilation_air_conditioning_systems[*].fan_system.supply_air_temperature_reset_schedule",
        "$.ruleset_model_descriptions[*].heating_ventilation_air_conditioning_systems[*].fan_system.operating_schedule",
    ]

    referenced_id_list = find_all_by_jsonpaths(schedule_reference_jsonpaths, rpd)

    for schedule_id in referenced_id_list:
        if schedule_id not in schedule_id_list:
            mismatch_list.append(schedule_id)
    return mismatch_list


def check_fluid_loop_or_piping_association(rpd: dict) -> list:
    """
    Check the association between fluid loops or piping and pumps that reference them.
    Parameters
    ----------
    rpd

    Returns list of mismatched fluid loop or piping ids
    -------

    """
    mismatch_list = []
    fluid_loop_or_piping_id_jsonpaths = [
        "$.ruleset_model_descriptions[*].fluid_loops[*].id",
        "$.ruleset_model_descriptions[*].service_water_heating_distribution_systems[*].service_water_piping.id",
        "$.ruleset_model_descriptions[*].fluid_loops[*].child_loops[*].id",
    ]

    fluid_loop_or_piping_id_list = find_all_by_jsonpaths(
        fluid_loop_or_piping_id_jsonpaths, rpd
    )

    referenced_fluid_loop_or_piping_id_list = find_all(
        "$.ruleset_model_descriptions[*].pumps[*].loop_or_piping",
        rpd,
    )
    for fluid_loop_or_piping_id in referenced_fluid_loop_or_piping_id_list:
        if fluid_loop_or_piping_id not in fluid_loop_or_piping_id_list:
            mismatch_list.append(fluid_loop_or_piping_id)
    return mismatch_list


def check_service_water_heating_association(rpd):
    """
    Check the association between service water heating distribution systems and the various objects that reference them.
    Parameters
    ----------
    rpd

    Returns list of mismatched service water heating distribution system ids
    -------

    """
    mismatch_list = []
    service_water_heating_id_list = find_all(
        "$.ruleset_model_descriptions[*].service_water_heating_distribution_systems[*].id",
        rpd,
    )

    service_water_heating_reference_jsonpaths = [
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*].served_by_distribution_system",
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].served_by_service_water_heating_system",
        "$.ruleset_model_descriptions[*].service_water_heating_equipment[*].distribution_system",
    ]

    referenced_service_water_heating_id_list = find_all_by_jsonpaths(
        service_water_heating_reference_jsonpaths, rpd
    )

    for service_water_heating_id in referenced_service_water_heating_id_list:
        if service_water_heating_id not in service_water_heating_id_list:
            mismatch_list.append(service_water_heating_id)
    return mismatch_list


# search schedule with keywords: Constraint to use when implemented :


def check_hvac_association(rpd: dict) -> list:
    """
    Check the association between hvac systems and the terminals served by HVAC systems.
    Parameters
    ----------
    rpd

    Returns list of mismatched hvac ids
    -------

    """
    mismatch_list = []
    hvac_id_list = find_all(
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
        rpd,
    )
    served_by_hvac_id_list = find_all(
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*].terminals[*].served_by_heating_ventilating_air_conditioning_system",
        rpd,
    )
    for hvac_id in served_by_hvac_id_list:
        if hvac_id not in hvac_id_list:
            mismatch_list.append(hvac_id)
    return mismatch_list


def check_annual_schedule_lengths(rpd: dict) -> list[str]:
    """
    Verify that all schedules in the rpd file have the same length for hourly_values: either 8760 or 8784 entries.

    Parameters
    ----------
    rpd : dict
        The ruleset model description object.

    Returns
    -------
    list[str]
        A list of error messages for schedules that do not have 8760 or 8784 entries.
    """
    error_messages = []

    schedules = find_all(
        "$.ruleset_model_descriptions[*].schedules[?(@.hourly_values)]", rpd
    )
    lengths = [len(schedule) for schedule in schedules]

    if not lengths:
        return []  # No schedules with hourly_values — no errors

    # Compute the mode of the lengths
    length_counts = Counter(lengths)
    common_length, _ = length_counts.most_common(1)[0]

    # Check if common length is valid
    if common_length not in (8760, 8784):
        error_messages.append(
            f"The most common schedule length is {common_length}, which is not 8760 or 8784."
        )

    for schedule, length in zip(schedules, lengths):
        schedule_id = schedule.get["id"]
        if length != common_length:
            error_messages.append(
                f"Schedule '{schedule_id}' has {length} hourly values; expected {common_length}."
            )

    return error_messages


def check_unique_ids_in_ruleset_model_descriptions(rpd):
    """Checks that the ids within each group inside a
    RuleSetModelInstance are unique

    The strategy is to first find all unique json paths to all lists inside the
    RuleSetModelInstance, with all list indexes set to [*]. For example,
    the general jsonpath to the building_segments is "buildings[*].building_segments".
    Then, for each of these unique list_paths, we use find_all using the jsonpath
    list_path[*].id to find all the ids for this path and check that they are unique.

    Parameters
    ----------
    rpd : dict
        A dictionary representing an RPD

    Returns
    -------
    str
        An error message listing any paths that do not have unique ids. The empty string
        indicates that all appropriate ids are unique.
    """
    # The schema does not require the ruleset_model_descriptions field, default to []
    ruleset_model_descriptions = rpd.get("ruleset_model_descriptions", [])

    bad_paths = []
    for rmd_index, rmd in enumerate(ruleset_model_descriptions):
        # Collect all jsonpaths to lists
        paths = json_paths_to_lists(rmd)

        for list_path in paths:
            ids = find_all(list_path + "[*].id", rmd)
            if len(ids) != len(set(ids)):
                # The ids are not unique
                # list_path starts with "$" that must be removed
                bad_path = f"ruleset_model_descriptions[{rmd_index}]{list_path[1:]}"
                bad_paths.append(bad_path)

    error_msg = f"Non-unique ids for paths: {'; '.join(bad_paths)}" if bad_paths else ""

    return error_msg


def json_paths_to_lists(val, path="$"):
    """Determines all the generic json paths to lists inside an object

    If a json path has a list index, that index is replaced with [*] to make it
    generic.

    Parameters
    ----------
    val : any
        Only dict and list objects are processed, all others are ignored
    path : str
        A json path representing a generic path to val in a larger structure

    Returns
    -------
    set
        A set of unique generic json paths to lists inside val
    """
    paths = set()
    if isinstance(val, dict):
        paths = json_paths_to_lists_from_dict(val, path)
    elif isinstance(val, list):
        paths = json_paths_to_lists_from_list(val, path)

    return paths


def json_paths_to_lists_from_dict(rmd_dict, path):
    """Determines all the generic json paths to lists inside a dictionary

    If a json path has a list index, that index is replaced with [*] to make it
    generic.

    Parameters
    ----------
    rmd_dict : dict

    path : str
        A json path representing a generic path to rmd_dict in a larger structure

    Returns
    -------
    set
        A set of unique generic json paths to lists inside rmd_dict
    """
    paths = set()
    for key, val in rmd_dict.items():
        new_path = f"{path}.{key}"
        new_paths = json_paths_to_lists(val, new_path)
        paths = paths.union(new_paths)

    return paths


def json_paths_to_lists_from_list(rmd_list, path):
    """Determines all the generic json paths to lists inside a list

    If a json path has a list index, that index is replaced with [*] to make it
    generic.

    Parameters
    ----------
    rmd_list : list

    path : str
        A json path representing a generic path to rmd_list in a larger structure

    Returns
    -------
    set
        A set of unique generic json paths to lists inside rmd_list
    """
    paths = {path}
    for val in rmd_list:
        new_path = f"{path}[*]"
        new_paths = json_paths_to_lists(val, new_path)
        paths = paths.union(new_paths)

    return paths


def non_schema_validate_rpd(rmd_obj):
    """Provides non-schema validation for an RMD"""
    error = []
    unique_id_error = check_unique_ids_in_ruleset_model_descriptions(rmd_obj)
    passed = not unique_id_error
    if not passed:
        error.append(unique_id_error)

    mismatch_hvac_errors = check_hvac_association(rmd_obj)
    passed = passed and not mismatch_hvac_errors
    if mismatch_hvac_errors:
        error.append(
            f"Cannot find HVAC systems {mismatch_hvac_errors} in the HeatingVentilationAirConditioningSystems data group."
        )

    mismatch_zone_errors = check_zone_association(rmd_obj)
    passed = passed and not mismatch_zone_errors
    if mismatch_zone_errors:
        error.append(
            f"Cannot find zones {mismatch_zone_errors} in the Zone data group."
        )

    mismatch_fluid_loop_errors = check_fluid_loop_association(rmd_obj)
    passed = passed and not mismatch_fluid_loop_errors
    if mismatch_fluid_loop_errors:
        error.append(
            f"Cannot find fluid loop {mismatch_fluid_loop_errors} in the FluidLoop data group."
        )

    mismatch_schedule_errors = check_schedule_association(rmd_obj)
    passed = passed and not mismatch_schedule_errors
    if mismatch_schedule_errors:
        error.append(
            f"Cannot find schedule {mismatch_schedule_errors} in the Schedule data group."
        )

    mismatch_fluid_loop_piping_errors = check_fluid_loop_or_piping_association(rmd_obj)
    passed = passed and not mismatch_fluid_loop_piping_errors
    if mismatch_fluid_loop_piping_errors:
        error.append(
            f"Cannot find piping {mismatch_schedule_errors} in the FluidLoop or ServiceWaterHeatingDistributionSystems data group."
        )

    mismatch_service_water_heating_errors = check_service_water_heating_association(
        rmd_obj
    )
    passed = passed and not mismatch_service_water_heating_errors
    if mismatch_service_water_heating_errors:
        error.append(
            f"Cannot find service water heating {mismatch_service_water_heating_errors} in the ServiceWaterHeatingDistributionSystems data group."
        )

    mismatch_associated_data_elements_errors = check_associated_data_elements(rmd_obj)
    passed = passed and not mismatch_associated_data_elements_errors
    if mismatch_associated_data_elements_errors:
        error.extend(mismatch_associated_data_elements_errors)

    mismatch_annual_schedule_length_errors = check_annual_schedule_lengths(rmd_obj)
    passed = passed and not mismatch_annual_schedule_length_errors
    if mismatch_annual_schedule_length_errors:
        error.extend(mismatch_annual_schedule_length_errors)

    return {"passed": passed, "error": error if error else None}


def schema_validate_rpd(rpd, full_errors: bool = False):
    """Validates an RMD against the schema

    This code follows the outline given in
    https://stackoverflow.com/questions/53968770/how-to-set-up-local-file-references-in-python-jsonschema-document
    """

    # Load the schema files
    with open(SCHEMA_PATH) as json_file:
        schema = json.load(json_file)
    with open(SCHEMA_ENUM_PATH) as json_file:
        schema_enum = json.load(json_file)
    with open(SCHEMA_T24_ENUM_PATH) as json_file:
        schema_t24_enum = json.load(json_file)
    with open(SCHEMA_RESNET_ENUM_PATH) as json_file:
        schema_resnet_enum = json.load(json_file)
    with open(SCHEMA_OUTPUT_PATH) as json_file:
        schema_output = json.load(json_file)

    registry = Registry().with_resources(
        [
            ("ASHRAE229.schema.json", DRAFT7.create_resource(schema)),
            (
                "Enumerations2019ASHRAE901.schema.json",
                DRAFT7.create_resource(schema_enum),
            ),
            (
                "Enumerations2019T24.schema.json",
                DRAFT7.create_resource(schema_t24_enum),
            ),
            (
                "EnumerationsRESNET.schema.json",
                DRAFT7.create_resource(schema_resnet_enum),
            ),
            ("Output2019ASHRAE901.schema.json", DRAFT7.create_resource(schema_output)),
        ]
    )
    try:
        # Validate the RPD against the schema
        validator = Draft7Validator(schema, registry=registry)
        Draft7Validator.check_schema(schema)
        errors = list(validator.iter_errors(rpd))

        if errors:
            error_details = []
            for error in errors:
                # Convert absolute paths to JSONPath format
                error_path = convert_absolute_path_list_to_jsonpath(
                    list(error.absolute_path)
                )
                parent_id_path = format_jsonpath_with_id(list(error.absolute_path))
                parent_id = find_all(parent_id_path, rpd) if parent_id_path else ""

                # Construct the error message
                parent_id = parent_id[0] if parent_id else parent_id
                if not full_errors:
                    truncated_message = (
                        (error.message[:20] + ".........." + error.message[-130:])
                        if len(error.message) > 160
                        else error.message
                    )
                    error_message = f"{truncated_message}. Path: {error_path}." + (
                        f" Parent ID: {parent_id}" if parent_id else ""
                    )
                else:
                    error_message = f"{error.message}. Path: {error_path}." + (
                        f" Parent ID: {parent_id}" if parent_id else ""
                    )
                error_details.append(error_message)

            return {"passed": False, "errors": error_details}

        return {"passed": True, "errors": []}  # No errors found

    except Exception as error:
        return {"passed": False, "errors": [f"Unexpected error: {str(error)}"]}


def validate_rpd(rpd, test=False):
    """Validate an RMD against the schema and other high-level checks"""
    # Validate against the schema
    result = schema_validate_rpd(rpd)

    if result["passed"] and not test:
        # Only check if it is not software test workflow.
        # Provide non-schema validation
        result = non_schema_validate_rpd(rpd)

    return result
