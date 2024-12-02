from rct229.rulesets.ashrae9012019.data_fns.extra_schema_fns import (
    EXTRA_SCHEMA,
    compare_context_pair,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_associated_with_each_swh_distriubtion_system import (
    get_swh_equipment_associated_with_each_swh_distribution_system,
)
from rct229.utils.assertions import assert_
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
    swh_distribution_id: str


    Returns
    -------

    """
    errors = []

    rmd1_swh_system_and_equip_dict = (
        get_swh_equipment_associated_with_each_swh_distribution_system(rmd1)
    )
    rmd2_swh_system_and_equip_dict = (
        get_swh_equipment_associated_with_each_swh_distribution_system(rmd2)
    )

    # assert_(
    #     rmd1_swh_system_and_equip_dict[swh_distribution_id]
    #     or rmd2_swh_system_and_equip_dict[swh_distribution_id],
    #     f"SWH Distribution System {swh_distribution_id} not found in one of the two RMDs",
    # )
    # assert_(
    #     rmd1_swh_system_and_equip_dict[swh_distribution_id]
    #     and rmd2_swh_system_and_equip_dict[swh_distribution_id],
    #     f"SWH Distribution System {swh_distribution_id} not found in one of the two RMDs",
    # )

    if rmd1_swh_system_and_equip_dict.get(swh_distribution_id):
        rmd1_swh_equipment_dict = rmd1_swh_system_and_equip_dict[swh_distribution_id]
        rmd1_swh_distribution = (
            find_exactly_one_service_water_heating_distribution_system(
                rmd1, swh_distribution_id
            )
        )
    if rmd2_swh_system_and_equip_dict.get(swh_distribution_id):
        rmd2_swh_equipment_dict = rmd2_swh_system_and_equip_dict[swh_distribution_id]
        rmd2_swh_distribution = (
            find_exactly_one_service_water_heating_distribution_system(
                rmd2, swh_distribution_id
            )
        )

    if len(rmd1_swh_distribution) > len(rmd2_swh_distribution):
        index_content_list = rmd1_swh_distribution
        compare_context_list = rmd2_swh_distribution
    else:
        index_content_list = rmd2_swh_distribution
        compare_context_list = rmd1_swh_distribution

    # swh equipment
    assert_(
        len(rmd1_swh_equipment_dict.swh_heating_eq)
        == len(rmd2_swh_equipment_dict.swh_heating_eq),
        f"Unequal numbers of SWH Equipment between the two models for {swh_distribution_id}",
    )

    for swh_eq_id in rmd1_swh_equipment_dict.swh_heating_eq:
        swh_eq_1 = find_exactly_one_service_water_heating_equipment(rmd1, swh_eq_id)
        swh_eq_2 = find_exactly_one_service_water_heating_equipment(rmd2, swh_eq_id)

        if len(swh_eq_1) > len(swh_eq_2):
            index_content_list = swh_eq_1
            compare_context_list = swh_eq_2
        else:
            index_content_list = swh_eq_2
            compare_context_list = swh_eq_1

        compare_context_pair(
            index_context=index_content_list,
            compare_context=compare_context_list,
            element_json_path="",
            extra_schema=EXTRA_SCHEMA["RulesetProjectDescription"]["Data Elements"],
            error_msg_list=errors,
            search_key=compare_context_str,
            required_equal=True,
        )

    # pump
    assert_(
        len(rmd1_swh_equipment_dict.pumps) == len(rmd2_swh_equipment_dict.pumps),
        f"Unequal number of pumps in the two models for SWH Distribution System {swh_distribution_id}",
    )

    for pump_id in rmd1_swh_equipment_dict.pumps:
        pump_1 = find_exactly_one_pump(rmd1, pump_id)
        pump_2 = find_exactly_one_pump(rmd2, pump_id)

        if len(pump_1) > len(pump_2):
            index_content_list = pump_1
            compare_context_list = pump_2
        else:
            index_content_list = pump_2
            compare_context_list = pump_1

        compare_context_pair(
            index_context=index_content_list,
            compare_context=compare_context_list,
            element_json_path="",
            extra_schema=EXTRA_SCHEMA["RulesetProjectDescription"]["Data Elements"],
            error_msg_list=errors,
            search_key=compare_context_str,
            required_equal=True,
        )

    return errors
