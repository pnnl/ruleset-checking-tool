from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value


def get_swh_equipment_associated_with_each_swh_bat(
    rmd: dict,
) -> dict[str, dict]:
    """
    This function gets all the SWH equipment connected to a particular SWH use type.  The information is stored in a dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 and values are a dictionary giving the ServiceWaterHeatingDistributionSystem, ServiceWaterHeatingEquipment, and Pumps connected to the particular use type.  There is also an entry for the total energy required to heat all SWH uses for a year: "EnergyRequired" .

    Parameters
    ----------
    rmd: dict, RMD at RuleSetModelDescription level
    Returns
    -------
    swh_and_equip_dict: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.
                        Example:  {"DORMITORY":{"SWHDistribution":["swhd1","swhd2"], "SWHHeatingEq":["swh_eq1","swh_eq2"], "Pumps":["p1"], "Tanks":["t1"], "Piping":["piping1"], "SolarThermal":[], "SWH_Uses":["swh_use1","swh_use2"], "EnergyRequired": 100000}}
    """

    swh_and_equip_dict = {}
    for building_segment in find_all("$.buildings[*].building_segments[*]", rmd):
        swh_bat = get_building_segment_swh_bat(rmd, building_segment)
        swh_and_equip_dict[swh_bat].set_default(
            {
                "SWHDistribution": [],
                "SWHHeatingEq": [],
                "Pumps": [],
                "Tanks": [],
                "Piping": [],
                "SolarThermal": [],
                "SWH_Uses": [],
                "EnergyRequired": 0,
            }
        )

        service_water_heating_use_ids = (
            get_SWH_uses_associated_with_each_building_segment(
                rmd, building_segment["id"]
            )
        )
        for swh_use_id in service_water_heating_use_ids:

            swh_use = find_exactly_one_with_field_value(
                "$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*]",
                "id",
                swh_use_id,
                rmd,
            )
            energy_required = get_energy_required_to_heat_swh_use(
                swh_use, rmd, building_segment
            )
            swh_and_equip_dict[swh_bat]["EnergyRequired"] += energy_required
            swh_and_equip_dict[swh_bat]["SWH_Uses"].append(swh_use.id)
            distribution_id = swh_use.get("served_by_distribution_system")
            if distribution_id not in swh_and_equip_dict[swh_bat]["SWHDistribution"]:
                swh_and_equip_dict[swh_bat]["SWHDistribution"].append(distribution_id)

                distribution = find_exactly_one_with_field_value(
                    "$.service_water_heating_distribution_systems[*]",
                    "id",
                    distribution_id,
                    rmd,
                )
                tanks = distribution.get("tanks")
                for tank in tanks:
                    swh_and_equip_dict[swh_bat]["Tanks"].append(tank["id"])

                for piping_id in distribution.get("service_water_piping"):
                    piping_ids = get_all_child_SWH_piping_ids(rmd, piping_id)
                    swh_and_equip_dict[swh_bat]["Piping"].extend(piping_ids)

        for swh_bat in swh_and_equip_dict:
            for pump in find_all("$.pumps[*]", rmd):
                if pump.get("loop_or_piping") in swh_and_equip_dict[swh_bat]["Piping"]:
                    swh_and_equip_dict[swh_bat]["Pumps"].append(pump["id"])

            for swh_equip in find_all("$.service_water_heating_equipment[*]", rmd):
                if (
                    swh_equip.get("distribution_system")
                    in swh_and_equip_dict[swh_bat]["SWHDistribution"]
                ):
                    swh_and_equip_dict[swh_bat]["SWHHeatingEq"].append(swh_equip["id"])
                    for solar_t in swh_equip.get("solar_thermal_systems"):
                        swh_and_equip_dict[swh_bat]["SolarThermal"].append(
                            solar_t["id"]
                        )

    return swh_and_equip_dict
