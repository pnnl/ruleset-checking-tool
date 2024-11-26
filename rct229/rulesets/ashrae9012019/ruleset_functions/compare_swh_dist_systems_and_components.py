from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_associated_with_each_swh_distriubtion_system import (
    get_swh_equipment_associated_with_each_swh_distribution_system,
)
from rct229.utils.assertions import assert_


def compare_swh_dist_systems_and_components(
    RMD1: dict, RMD2: dict, compare_context_str: str, swh_distribution_id: str
):
    """
    Parameters
    ----------
    RMD1: dict
        RMD at RuleSetModelDescription level
    RMD2: dict
        RMD at RuleSetModelDescription level
    compare_context_str: str
    swh_distribution_id: str


    Returns
    -------

    """
    RMD1_swh_system_and_equip_dict = (
        get_swh_equipment_associated_with_each_swh_distribution_system(RMD1)
    )
    RMD2_swh_system_and_equip_dict = (
        get_swh_equipment_associated_with_each_swh_distribution_system(RMD2)
    )

    assert_(
        RMD1_swh_system_and_equip_dict[swh_distribution_id]
        or RMD2_swh_system_and_equip_dict[swh_distribution_id],
        f"SWH Distribution System {swh_distribution_id} not found in one of the two RMDs",
    )
    assert_(
        RMD1_swh_system_and_equip_dict[swh_distribution_id]
        and RMD2_swh_system_and_equip_dict[swh_distribution_id],
        f"SWH Distribution System {swh_distribution_id} not found in one of the two RMDs",
    )

    if RMD1_swh_system_and_equip_dict.get(swh_distribution_id):
        RMD1_swh_equipment_dict = RMD1_swh_system_and_equip_dict[swh_distribution_id]
        RMD1_swh_distribution = 1
    if RMD2_swh_system_and_equip_dict.get(swh_distribution_id):
        RMD2_swh_equipment_dict = RMD2_swh_system_and_equip_dict[swh_distribution_id]
        RMD2_swh_distribution = 1

    if len(RMD1_swh_distribution) > len(RMD2_swh_distribution):
        index_content_list = RMD1_swh_distribution
        compare_context_list = RMD2_swh_distribution
    else:
        index_content_list = RMD2_swh_distribution
        compare_context_list = RMD1_swh_distribution

    assert_(
        len(RMD1_swh_equipment_dict["SWHHeatingEq"])
        == len(RMD2_swh_equipment_dict["SWHHeatingEq"]),
        "Unequal numbers of SWH Equipment between the two models for {swh_distribution_id}",
    )

    for swh_eq_id in RMD1_swh_equipment_dict["SWHHeatingEq"]:
        # swh_eq_1 = get_component_by_id(rmd1, swh_eq_id)
        # swh_eq_2 = get_component_by_id(rmd2, swh_eq_id)
        swh_eq_1 = 1
        swh_eq_2 = 2

        if len(swh_eq_1) > len(swh_eq_2):
            index_content_list = swh_eq_1
            compare_context_list = swh_eq_2
        else:
            index_content_list = swh_eq_2
            compare_context_list = swh_eq_1

        compare_context_pair(index_context=index_content_list, compare_context=compare_context_list,
                             extra_schema='extra_schema_for_SWH_comparison.json', error_msg_list=errors,
                             search_key=compare_context_str): errors.append(
            "Comparison of SWH Equipment: " + swh_eq_id + " failed.")

    assert_(
        len(RMD1_swh_equipment_dict["Pumps"]) == len(RMD2_swh_equipment_dict["Pumps"]),
        f"Unequal number of pumps in the two models for SWH Distribution System {swh_distribution_id}",
    )

    for pump_id in RMD1_swh_equipment_dict["Pumps"]:
        pump_1 = get_component_by_id(RMD1, pump_id)
        pump_2 = get_component_by_id(RMD2, pump_id)

        if len(pump_1) > len(pump_2):
            index_content_list = pump_1
            compare_context_list = pump_2
        else:
            index_content_list = pump_2
            compare_context_list = pump_1

        compare_context_pair(index_context=index_content_list, compare_context=compare_context_list,
                             extra_schema='extra_schema_for_SWH_comparison.json', error_msg_list=errors,
                             search_key=compare_context_str)


    return
