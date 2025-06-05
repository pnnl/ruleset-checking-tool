from rct229.rulesets.ashrae9012019.data_fns.extra_schema_fns import (
    EXTRA_SCHEMA,
    compare_context_pair,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_associated_with_each_swh_distriubtion_system import (
    get_swh_equipment_associated_with_each_swh_distribution_system,
)
from rct229.utils.utility_functions import (
    find_exactly_one_pump,
    find_exactly_one_service_water_heating_distribution_system,
    find_exactly_one_service_water_heating_equipment,
)


def compare_swh_dist_systems_and_components(
    rmd1: dict, rmd2: dict, compare_context_str: str, swh_distribution_id: str
):
    """This function compares all sub-components of a given SWH Distribution System ID between two models.
    Parameters
    ----------
    rmd1: dict
        RMD at RuleSetModelDescription level
    rmd2: dict
        RMD at RuleSetModelDescription level
    compare_context_str: str
        compare context value from the extra schema (e.g., RMD Test, AppG Used By TCDs, AppG P_RMD Equals U_RMD, AppG B_RMD Equals P_RMD, AppG B_RMDs Same)
    swh_distribution_id: str
        id of the `service_water_heating_distribution_systems` key to compare

    Returns
    -------
    errors: list
        An array of errors encountered in this function and in compare_context_pair. If errors is an empty array, then all elements that were expected to match do match

    """

    errors_list = []
    rmd1_swh_system_and_equip_dict = (
        get_swh_equipment_associated_with_each_swh_distribution_system(rmd1)
    )
    rmd2_swh_system_and_equip_dict = (
        get_swh_equipment_associated_with_each_swh_distribution_system(rmd2)
    )

    rmd1_swh_distribution = None
    rmd2_swh_distribution = None
    # service_water_heating_distribution_systems
    if not rmd1_swh_system_and_equip_dict.get(swh_distribution_id):
        errors_list.append(
            f"SWH Distribution System {swh_distribution_id} not found in the `rmd1`."
        )
    else:
        rmd1_swh_distribution = (
            find_exactly_one_service_water_heating_distribution_system(
                rmd1, swh_distribution_id
            )
        )

    if not rmd2_swh_system_and_equip_dict.get(swh_distribution_id):
        errors_list.append(
            f"SWH Distribution System {swh_distribution_id} not found in the `rmd2`."
        )
    else:
        rmd2_swh_distribution = (
            find_exactly_one_service_water_heating_distribution_system(
                rmd2, swh_distribution_id
            )
        )

    if rmd1_swh_distribution and rmd2_swh_distribution:
        compare_context_pair(
            index_context=rmd1_swh_distribution,
            compare_context=rmd2_swh_distribution,
            element_json_path=f"$.service_water_heating_distribution_systems[{swh_distribution_id}]",
            extra_schema=EXTRA_SCHEMA["ServiceWaterHeatingDistributionSystem"][
                "Data Elements"
            ],
            error_msg_list=errors_list,
            search_key=compare_context_str,
            required_equal=True,
        )

        # service_water_heating_equipment
        rmd1_swh_equipment_dict = rmd1_swh_system_and_equip_dict[swh_distribution_id]
        rmd2_swh_equipment_dict = rmd2_swh_system_and_equip_dict[swh_distribution_id]
        if len(rmd1_swh_equipment_dict.swh_heating_eq) != len(
            rmd2_swh_equipment_dict.swh_heating_eq
        ):
            errors_list.append(
                f"Unequal numbers of SWH Equipment between the two models for {swh_distribution_id}"
            )

        for swh_eq_id in rmd1_swh_equipment_dict.swh_heating_eq:
            swh_eq_1 = find_exactly_one_service_water_heating_equipment(rmd1, swh_eq_id)
            swh_eq_2 = find_exactly_one_service_water_heating_equipment(rmd2, swh_eq_id)

            if swh_eq_1 is None or swh_eq_2 is None:
                errors_list.append(
                    f"`service_water_heating_equipment (id: {swh_eq_id})` doesn't exist in the rmd argument."
                )
            else:
                compare_context_pair(
                    index_context=swh_eq_1,
                    compare_context=swh_eq_2,
                    element_json_path=f"$.service_water_heating_equipment[{swh_eq_id}]",
                    extra_schema=EXTRA_SCHEMA["ServiceWaterHeatingEquipment"][
                        "Data Elements"
                    ],
                    error_msg_list=errors_list,
                    search_key=compare_context_str,
                    required_equal=True,
                )

        # pumps
        if len(rmd1_swh_equipment_dict.pumps) != len(rmd2_swh_equipment_dict.pumps):
            errors_list.append(
                f"Unequal number of pumps in the two models for SWH Distribution System {swh_distribution_id}"
            )

        for pump_id in rmd1_swh_equipment_dict.pumps:
            pump_1 = find_exactly_one_pump(rmd1, pump_id)
            pump_2 = find_exactly_one_pump(rmd2, pump_id)

            if pump_1 is None or pump_2 is None:
                errors_list.append(f"`pumps`object doesn't exist in the rmd argument.")
            else:
                compare_context_pair(
                    index_context=pump_1,
                    compare_context=pump_2,
                    element_json_path=f"$.pumps[{pump_id}]",
                    extra_schema=EXTRA_SCHEMA["Pump"]["Data Elements"],
                    error_msg_list=errors_list,
                    search_key=compare_context_str,
                    required_equal=True,
                )

    return errors_list
