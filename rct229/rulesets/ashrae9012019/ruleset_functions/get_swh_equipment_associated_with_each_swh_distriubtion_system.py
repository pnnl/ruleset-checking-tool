from rct229.utils.jsonpath_utils import find_all


def get_SWH_equipment_associated_with_each_swh_distribution_system(
    rmd: dict,
) -> dict[str, dict]:
    """
    This function gets all the SWH equipment connected to a SWH distribution system.  The information is stored in a dictionary where the keys are the SWH Distribution System Ids and values are a dictionary giving the ServiceWaterHeatingEquipment, and Pumps connected to the particular SWH distribution system.
    Parameters
    ----------
    rmd: dict, RMD at RuleSetModelDescription level
    Returns
    -------
    swh_and_equip_dict: A dictionary containing where the keys are the SWH Distribution System IDs and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.
                        Example:  {"swh_distribution1":{"swh_heating_eq":["swh_eq1","swh_eq2"], "pumps":["p1"], "tanks":["t1"], "piping":["piping1"], "solar_thermal":[], "uses":["sp1_use","sp2_use"], "spaces_served":[sp1,sp2]}}
    """

    swh_and_equip_dict = {}
    for distribution in find_all(
        "$.service_water_heating_distribution_systems[*]", rmd
    ):
        swh_and_equip_dict.setdefault(
            distribution["id"],
            {
                "SWHHeatingEq": [],
                "Pumps": [],
                "Tanks": [],
                "Piping": [],
                "SolarThermal": [],
                "USES": [],
                "SPACES_SERVED": [],
            },
        )
        tanks = distribution.get("tanks")
        for tank in tanks:
            swh_and_equip_dict[distribution["id"]]["Tanks"].append(tank["id"])

        pipings = distribution.get("service_water_piping")
        for piping in pipings:
            piping_ids = get_all_child_SWH_piping_ids(rmd, piping["id"])
            swh_and_equip_dict[distribution["id"]]["Piping"].extend(piping_ids)

        for pump in find_all("$.pumps[*]", rmd):
            if (
                pump.get("loop_or_piping")
                in swh_and_equip_dict[distribution["id"]]["Piping"]
            ):
                swh_and_equip_dict[distribution["id"]]["Pumps"].append(pump["id"])

        for swh_equip in find_all("$.service_water_heating_equipment[*]", rmd):
            if swh_equip.get("distribution_system") == distribution["id"]:
                swh_and_equip_dict[distribution["id"]]["SWHHeatingEq"].append(
                    swh_equip["id"]
                )
            for solar_t in swh_equip.get("solar_thermal_systems"):
                swh_and_equip_dict[distribution["id"]]["SolarThermal"].append(
                    solar_t["id"]
                )

    for swh_use in find_all(
        "$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*]",
        rmd,
    ):
        distribution = swh_use.get("served_by_distribution_system")
        swh_and_equip_dict[distribution["id"]]["USES"].append(swh_use["id"])
        swh_and_equip_dict[distribution.id]["SPACES_SERVED"].append(
            space["id"] for space in get_spaces_served_by_SWH_use(rmd, swh_use["id"])
        )

    return swh_and_equip_dict
